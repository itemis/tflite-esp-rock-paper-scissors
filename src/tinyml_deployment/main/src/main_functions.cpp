#include <stdio.h>
#include <iostream>
#include <vector>
#include <stdint.h>


#include <cstdlib>
#include <ctime> 

#include "main_functions.h"
#include "DataProvider.h"
#include "FeatureProvider.h"
#include "model_weights.h" // C-string with trained model weights
#include "PredictionHandler.h"
#include "PredictionInterpreter.h"
#include "tensorflow/lite/micro/kernels/micro_ops.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
// version.h is missing in https://github.com/espressif/tflite-micro-esp-examples
// #include "tensorflow/lite/version.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define pdSECOND pdMS_TO_TICKS(1000)

namespace{
    // declare ErrorReporter, a TfLite class for error logging
    tflite::ErrorReporter *error_reporter = nullptr;
    const tflite::Model *model = nullptr; // declare model
    // declare interpreter, runs inference using model and data
    tflite::MicroInterpreter *interpreter = nullptr;
    // declare model input and output, two tensors as arrays
    TfLiteTensor *model_input = nullptr;
    TfLiteTensor *model_output = nullptr;

    // Create an area of memory to use for input, output, and intermediate arrays.
    // The size of this will depend on the model you're using, and may need to be
    // determined by experimentation.
    //
    // This model claims it requires 135 * 1024 = 138240 bytes,
    // however exactly allocating that much is not sufficient,
    // about 4416 bytes more are needed,
    // so we add 5*1024 on top.
    constexpr int kTensorArenaSize = 140 * 1024;

    // alignas forces multiples of 16 to be the only valid memory addresses
    // only applies to the tensor_arena array
    // tensor arena is where model is loaded and inference happens
    alignas(16) uint8_t tensor_arena[kTensorArenaSize];
}

DataProvider data_collector; // receive data from sensors
FeatureProvider data_processor; // preprocess sensor data
PredictionInterpreter prediction_interpreter;
PredictionHandler prediction_handler;

// pretty printing
bool first_round = true;
uint8_t num_classes = 3;



void setup(){
    // random number generation
    srand(time(NULL));

    // adaptation of TfLite ErrorReporter for MCUs
    static tflite::MicroErrorReporter micro_error_reporter;
    error_reporter = &micro_error_reporter; // set error reporter

    // import the trained weights from the C string
    model = tflite::GetModel(model_weights);
    // assert that model schema version and tflite version match
    if (model->version() != TFLITE_SCHEMA_VERSION) {
    TF_LITE_REPORT_ERROR(error_reporter,
                         "Model provided is schema version %d not equal "
                         "to supported version %d.",
                         model->version(), TFLITE_SCHEMA_VERSION);
    return;
    }

    // load all tflite micro built-in operations
    // for example layers, activation functions, pooling
    static tflite::AllOpsResolver resolver;
    
    // initialize interpreter
    static tflite::MicroInterpreter static_interpreter(
        model, resolver, tensor_arena, kTensorArenaSize, error_reporter);
    interpreter = &static_interpreter;

    // interpreter knows all data shapes
    // can allocate memory (tensors)
    TfLiteStatus allocate_status = interpreter->AllocateTensors();
    if (allocate_status != kTfLiteOk) {
        TF_LITE_REPORT_ERROR(error_reporter, "AllocateTensors() failed\n");
        return;
    }

    // shorten namespace
    model_input = interpreter->input(0);
    model_output = interpreter->output(0);
    // assert real input matches expect input
    if ((model_input->dims->size != 4) || // tensor of shape (1, 96, 96, 1) has dim 4
        (model_input->dims->data[0] != 1) || // 1 img per batch
        (model_input->dims->data[1] != 96) || // 96 x pixels
        (model_input->dims->data[2] != 96) || // 96 y pixels
        (model_input->dims->data[3] != 1) || // 1 channels
        (model_input->type != kTfLiteFloat32)) { // type of a single data point, here a pixel
            error_reporter->Report("Bad input tensor parameters in model\n");
        return;
        }

    // define periphery of MCU
    // what pins receive what data and in what way
    //data_collector.dataProviderBegin();
    vTaskDelay(1 * pdSECOND); // FreeRTOS delay in seconds
}

bool isImgDark(uint8_t* img, uint8_t dim1, uint8_t dim2, uint8_t dim3){
    int32_t sum = 0;
    uint16_t len = dim1*dim2*dim3;
    for(uint16_t i = 0; i < len; i++) {
            sum += img[i];
    }
    float average = (float)sum / len;
    if (average < 33) return true;
    return false;
}

void makePrediction(uint8_t* img) {
    // read image from camera into a 1-dimensional array
    // the model converts 1-d array to expected dimension as encoded in weights
    if (kTfLiteOk != GetImage(error_reporter,
        data_collector.dim1, data_collector.dim2,
        data_collector.dim3, img)) {
        TF_LITE_REPORT_ERROR(error_reporter, "Image capture failed.");
    }

    // convert static array to vector
    // num of elements = total bytes / bytes of single element
    // start address + num of elements -> address space to reserve
    //std::vector<uint8_t> img_vec(img, img + sizeof(img) / sizeof(img[0]));
    std::vector<uint8_t> img_vec(img, img + data_collector.dim1*data_collector.dim2*data_collector.dim3);
    // convert uint8 vector to float vector 
    std::vector<float> img_float(img_vec.begin(), img_vec.end());
    // pass image to model
    std::copy(img_float.begin(), img_float.end(),  model_input->data.f);

    // apply inference through the model
    // write result to output tensor
    TfLiteStatus invoke_status = interpreter->Invoke();
    if (invoke_status != kTfLiteOk) {
        error_reporter->Report("Invoke failed");
        return;
    }
}

uint8_t ensembleVote(uint8_t* img, uint8_t num_reps, float delay) {
    uint8_t class_count[] = {0, 0, 0};
    uint8_t player_move = 0;

    for (uint8_t i = 0; i < num_reps; i++) {
        makePrediction(img);
        player_move = prediction_interpreter.GetResult(model_output);
        class_count[player_move] += 1;
        vTaskDelay(delay * pdSECOND); // FreeRTOS delay in seconds
    }

    std::cout << "classcount:\n";
    for (int i = 0; i < 3; i++) {
        std::cout << unsigned(class_count[i]) << " ";
    }
    std::cout << "\n";
    
    return prediction_interpreter.argmax(class_count, 3);
}

void loop(){
    // declare static array to hold img
    uint8_t img[data_collector.dim1*data_collector.dim2*data_collector.dim3];

    // prints
    if (first_round == true) {   
        std::cout << "The game is about to start!\n\n";
        std::printf("################## first round! #################\n");
        first_round = false;
    }
    for (int i = 3; i > 0; i--) {
        std::cout << i << "!\n";
        vTaskDelay(1 * pdSECOND); // FreeRTOS delay in seconds
    }
    std::cout << "Show your hand!\n";
    vTaskDelay(1 * pdSECOND); // FreeRTOS delay in seconds

    // take multiple pictures and vote on most likely class
    uint8_t player_move = ensembleVote(img, 5, 0.2);
    prediction_handler.Update(player_move);


    while (
        isImgDark(img,
        data_collector.dim1,
        data_collector.dim2,
        data_collector.dim3)
    == false) {
        GetImage(error_reporter,
        data_collector.dim1, data_collector.dim2,
        data_collector.dim3, img);
        vTaskDelay(0.1 * pdSECOND); // FreeRTOS delay in seconds
    }
    
    std::printf("################## next round! #################\n");
    vTaskDelay(3 * pdSECOND); // FreeRTOS delay in seconds
}

