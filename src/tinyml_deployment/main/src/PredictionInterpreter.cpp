#include "PredictionInterpreter.h"
#include <stdio.h>
#include <iostream>

float PredictionInterpreter::max_in_array_float(float* arr, uint8_t len) {
    float m = 0;
    for (uint8_t i = 0; i < len; i++) {
        if (arr[i] >= m) m = arr[i];
    }
    return m;
}

uint8_t PredictionInterpreter::argmax_float(float* arr, uint8_t len) {
    float m = max_in_array_float(arr, len);
    for (uint8_t i = 0; i < len; i++) {
        if (arr[i] == m) return i;
    }
    return -1; // Error
}

uint8_t PredictionInterpreter::max_in_array(uint8_t* arr, uint8_t len) {
    uint8_t m = 0;
    for (uint8_t i = 0; i < len; i++) {
        if (arr[i] >= m) m = arr[i];
    }
    return m;
}



uint8_t PredictionInterpreter::argmax(uint8_t* class_count, uint8_t len) {
    uint8_t m = max_in_array(class_count, 3);
    for (uint8_t i = 0; i < len; i++) {
        if (class_count[i] == m) return i;
    }
    return -1; // Error
}

uint8_t PredictionInterpreter::GetResult(TfLiteTensor* model_output) {
    
    uint8_t player_move = 99;

    float paper = model_output->data.f[0];
    float rock = model_output->data.f[1];
    float scissors = model_output->data.f[2];
    std::cout << "interpretPrediction: " << "paper=" << paper << " rock=" << rock << " scissors=" << scissors << "\n";

    float pred_array[] = {paper, rock, scissors};
    player_move = argmax_float(pred_array, num_classes);
    std::cout << "interpretPrediction player_move: " << unsigned(player_move) << "\n";
    return player_move;

    // if (player_move == 0) {
    //     player_move_str = "paper";
    //     //print_ascii_paper();
    // }
    // if (player_move == 1) {
    //     player_move_str = "rock";
    //     //print_ascii_rock();
    // }
    // if (player_move == 2) {
    //     player_move_str = "scissors";
    //     //print_ascii_scissors();
    // }
}
