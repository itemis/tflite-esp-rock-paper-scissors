#!/bin/bash
echo "---- ---- ---- ---- ---- ----"
echo "---- ---- ---- UPDATING COMPONENTS"
echo "---- ---- ---- ---- ---- ----"

# make script executable form any path within project
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
COMPONENT_PATH=$SCRIPTPATH/components

# download submodules
git submodule update --init --recursive

# TFMICRO and ESP-NN components
# delete old components
rm -rf $COMPONENT_PATH/tfmicro
rm -rf $COMPONENT_PATH/esp-nn
rm -rf $COMPONENT_PATH/esp32-camera

# extract new components from submodule
cp -r $COMPONENT_PATH/sources/tflite-micro-esp-examples/components/tflite-lib $COMPONENT_PATH/tfmicro
cp -r $COMPONENT_PATH/sources/tflite-micro-esp-examples/components/esp-nn $COMPONENT_PATH/esp-nn
cp -r $COMPONENT_PATH/sources/tflite-micro-esp-examples/components/esp32-camera $COMPONENT_PATH/esp32-camera

# TODO:
# pull esp-nn from https://github.com/espressif/esp-nn/
# pull esp32-camera from https://github.com/espressif/esp32-camera/
# pull tfmicro from https://github.com/tensorflow/tensorflow

# add code for other dependencies here 
