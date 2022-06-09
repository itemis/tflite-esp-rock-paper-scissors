#!/bin/sh

# pipeline from model training to deployment on mcu
#python3 src/keras_model/main.py
python3 src/tf_lite_model/convert_to_tflite.py
./src/tf_lite_model/tflite_to_c_array.sh
python3 src/tf_lite_model/model_to_mcu.py
cd src/tinyml_deployment/
source ~/esp/esp-idf/export.sh # get_idf points there
cd src/tinyml_deployment/ # this or moving CMakeLists
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor