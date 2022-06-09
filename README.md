# Rock, Paper, Scissors on ESP-EYE using ESP-IDF, TfLite Micro, FreeRTOS

In this project we develop a model capable of discrimination between rock, paper and scissors visual inputs.
We provide a full pipeline starting with data collection, data augmentation, model training, model quantization and miniaturization to the deployment on a camera enabled microcontroller.
Each component can act independently and comes with a separate README.md file for explanation.
The components live under `src`.
Here we continue to list general software requirements for the entire pipeline.

## Requirements

### Python, model development

**Python**

Install Python. Version 3.10 is tested.

**Libraries option 1) pip, no virtual environment**

This is the easy option; packages are installed globally.

Install packages

    pip install -r requirements.txt

**Libraries option 2) Poetry**

Install Poetry.
Poetry manages packages and virtual environments for Python.

    # installation on linux
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    # activate poetry now
    source $HOME/.poetry/env

Install packages.

    poetry install

Enable virtual environment. Always necessary before invoking python from the shell, when using the poetry installation.

    poetry shell

Exit virtual environment

    exit

### Embedded C/C++, model deployment

**Espressif IDF**

Version 1.4 is tested.
Install via VSCode > Extensions > ESP-IDF > Express installation with all defaults.
At the end of the installation a command is shown.
This command should be executed to grant complete permissions.

**Libraries**

Next, download dependencies for the embedded system.

    chmod +x src/tinyml_deployment/update_components.sh
    ./src/tinyml_deployment/update_components.sh

### Respect the pipeline requirements

1. Data must be present in the `/data` directory in order to start training.
2. Preprocessing may be necessary.
3. A model must be trained and stored in `/bin_model`.
4. The model must be converted to a C array and included in the embedded code.

## Running

In order to train a model, convert it and flash to the MCU use the following script.

    chmod +x src/pipeline.sh
        ./src/pipeline.sh

### Data collection

For example, convert video footage to images, see `src/data_collection`.

    ffmpeg -i input.mp4 -vf fps=30 out%d.png

### Python, model development

Listed are the essential steps in the pipeline.
See local documentation for details.

#### Preprocessing

Starting from 600x600 color images and the following file structure.
For each of the preprocessing steps update name of `raw_images` in source code if necessary.

    data/
        raw_images/
            rock/
                rock1.png
                ...
            paper/
                ...
            scissors/
                ...

Number of images in each folder should be equal.

    python src/data_preprocessing/balance_classes.py

Reduce image size to 96x96 and convert to grayscale.

    python src/data_preprocessing/preprocess.py    

Split images into train and test sets.

    python src/data_preprocessing/split_data.py

#### Train a model

    python3 src/keras_model/main.py
    # model saved to /bin_model

#### Convert model

From TensorFlow format to TensorFlow lite.

    python3 src/tf_lite_model/convert_to_tflite.py

From TensorFlow lite to C array.

    chmod +x src/tf_lite_model/tflite_to_c_array.sh
    ./src/tf_lite_model/tflite_to_c_array.sh

Copy C array to embedded C/C++ code.

    python3 src/tf_lite_model/model_to_mcu.py

### Embedded C/C++, model deployment

Compile model and flash to device.

    cd src/tinyml_deployment && get_idf && idf.py build && idf.py -p /dev/ttyUSB0 flash monitor

# (Deprecated) Arduino IDE based

The Arduino approach is deprecated because the library `TensorFlowLite_ESP32` is not maintained.

## Requirements

- Arduino IDE. We use version 1.8.x. On Windows 11 the Microsoft Store Arduino IDE causes trouble when connecting from VSCode to the IDE. Optionally install VSCode with the Arduino extension for different IDE.

Install necessary libraries using the Arduino Library Manager.

- `TensorFlowLite_ESP32` support for the TensorFlow Lite Micro library via Arduino IDE on the ESP 32 Dev module and the ESP-EYE microcontroller.
- `DHT sensor library for ESPx` support for Elgoo 37 Sensor Kit V 2.0.
    
## Running

Configure the Arduino environment directly in the Arduino IDE or via the VSCode extension using keys `F1` or `CTRL+SHIFT+P`.

- Arduino: Select Serial Port. 

Probably `/dev/ttyUSB0` is the default.

- Arduino: Board Config.

Select your board type. We use the ESP-EYE V2.1. It is listed as AI Thinker ESP32-CAM.

Arduino: Verify.

    Select appropriate .ino file to verify. Typically the main file.

Arduino: Open Serial Monitor.

Arduino: Upload.

Arduino: Change Baud Rate.

    Unless specified otherwise its 115200.

Arduino: Close Serial Monitor.

    To stop reading incoming signals.
