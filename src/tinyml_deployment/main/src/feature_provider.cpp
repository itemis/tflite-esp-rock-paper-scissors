#include <vector>
#include <stdint.h>
#include "feature_provider.h"

// receive sensory data for preprocessing
void FeatureProvider::receiveData(std::vector<uint8_t> img){
    FeatureProvider::loaded_img = img;
}

// apply preprocessing
void FeatureProvider::processData(){

}

// return data to which preprocessing has already been applied
std::vector<uint8_t> FeatureProvider::forwardData(){
    return FeatureProvider::loaded_img;
}