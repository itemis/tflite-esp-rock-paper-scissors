#pragma once

#include <stdint.h>
#include <vector>

class FeatureProvider{
    public:
        FeatureProvider() = default;
        ~FeatureProvider() = default;
        void receiveData(std::vector<uint8_t>);
        void processData();
        std::vector<uint8_t> forwardData();

        std::vector<uint8_t> loaded_img; // currently processed image
};
