#!/bin/sh

# make script executable form any path within project
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
SRC_PATH=$SCRIPTPATH

# pipeline from model training to deployment on mcu
python3 $SRC_PATH/keras_model/main.py
python3 $SRC_PATH/tf_lite_model/convert_to_tflite.py
source $SRC_PATH/tf_lite_model/tflite_to_c_array.sh
python3 $SRC_PATH/tf_lite_model/model_to_mcu.py
cd $SRC_PATH/tinyml_deployment/
source ~/esp/esp-idf/export.sh # get_idf points there
cd $SRC_PATH/tinyml_deployment/ # this or moving CMakeLists
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
