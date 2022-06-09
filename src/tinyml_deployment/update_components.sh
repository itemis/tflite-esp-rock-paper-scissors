#!/bin/bash
git submodule update --init --recursive # download submodules

components=src/tinyml_deployment/components

# TFMICRO and ESP-NN components
# delete old components
rm -r $components/tfmicro
rm -r $components/esp-nn
rm -r $components/esp32-camera

# extract new components from submodule
cp -r $components/sources/tflite-micro-esp-examples/components/tflite-lib $components/tfmicro
cp -r $components/sources/tflite-micro-esp-examples/components/esp-nn $components/esp-nn
cp -r $components/sources/tflite-micro-esp-examples/components/esp32-camera $components/esp32-camera

# TODO:
# pull esp-nn from https://github.com/espressif/esp-nn/
# pull esp32-camera from https://github.com/espressif/esp32-camera/
# pull tfmicro from https://github.com/tensorflow/tensorflow

# add code for other dependencies here 