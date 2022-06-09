# Keras model to TFLite to C conversion

In the folder `keras_model` a model is built, trained and saved under the folder `bin_model`.
Afterwards use `convert_to_tf_lite.py` to convert the saved model.
Note, that the conversion doesn't apply to the model training snapshots saved in `h5` format but to the model folder containing proto-buffer `.pb` files.
The tflite model will also be saved under `bin_model` with a `.tflite` extension.
During the conversion quantization is applied to reduce the size of the model and make it suitable to run on microcontrollers.
Afterwards, the script `tflite_to_c_array.bash` is run to convert the `.tflite` file to a file called `model_hexgraph.cc` which is also stored to the `model_bin` folder.
File `model_hexgraph.cc` contains a static C-style array which encodes the trained weights of the keras model.

## Running

Ensure your path is the root of the project.

    cd path/to/project

Ensure that you have a Keras model.

    # should show a folder called keras_model
    ls bin_model
    # if not generate one using from src/keras_model/main.py

Conversion from Keras model to TFLite model.

    python src/tf_lite_model/convert_to_tflite.py

Conversion from TFLite model to C array.

    # chmod must only be run the first time you do this on your computer
    chmod +x src/tf_lite_model/tflite_to_c_array.bash
    ./src/tf_lite_model/tflite_to_c_array.bash

