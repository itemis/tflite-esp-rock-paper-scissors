#!/bin/sh

# make script executable form any path within project
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
SRC_PATH=$SCRIPTPATH

# pipeline from model training to deployment on mcu
python3 $SRC_PATH/keras_model/main.py
python3 $SRC_PATH/tf_lite_model/convert_to_tflite.py
bash $SRC_PATH/tf_lite_model/tflite_to_c_array.sh
python3 $SRC_PATH/tf_lite_model/model_to_mcu.py