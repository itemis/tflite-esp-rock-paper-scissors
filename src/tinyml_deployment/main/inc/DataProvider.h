#pragma once

#include <vector>
#include <stdint.h>

#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"

TfLiteStatus GetImage(tflite::ErrorReporter* error_reporter, int image_width,
                    int image_height, int channels, uint8_t* image_data);
/* a getter function that returns the camera specific context in which the image is captured */
void* image_provider_get_camera_fb();

class DataProvider{
    public:
        DataProvider() = default;
        ~DataProvider() = default;
        void printRGBImage(std::vector<uint8_t>, uint8_t, uint8_t, uint8_t);
        void printGrayImage(std::vector<uint8_t>, uint8_t, uint8_t);
        void dataProviderBegin();
        void gatherData();
        std::vector<uint8_t> forwardData();

        static const uint8_t dim1 = 96; // 96
        static const uint8_t dim2 = 96; // 96
        static const uint8_t dim3 = 1; // 3
        static const uint8_t tensorDim = 3;

        std::vector<uint8_t> loaded_img; // currently loaded image
};