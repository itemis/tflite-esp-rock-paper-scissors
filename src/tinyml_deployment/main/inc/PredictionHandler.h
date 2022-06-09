#pragma once

#include "PredictionInterpreter.h"

class PredictionHandler{
    public:
        PredictionHandler() = default;
        ~PredictionHandler() = default;
        void Update(uint8_t player_move);
    private:
};