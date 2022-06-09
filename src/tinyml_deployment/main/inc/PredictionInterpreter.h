#pragma once

#include "tensorflow/lite/c/common.h"

enum class Prediction {
    PAPER = 0,
    ROCK = 1,
    SCISSORS = 2
    // add your predictions
};

class PredictionInterpreter {
    public:
        uint8_t num_classes = 3;
        PredictionInterpreter() = default;
        ~PredictionInterpreter() = default;
        uint8_t argmax_float(float* arr, uint8_t len);
        float max_in_array_float(float* arr, uint8_t len);
        uint8_t argmax(uint8_t* class_count, uint8_t len);
        uint8_t max_in_array(uint8_t* arr, uint8_t len);
        virtual uint8_t GetResult(TfLiteTensor* model_output); // why virtual?
};