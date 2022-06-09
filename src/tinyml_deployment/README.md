# Deployment of model on microcontroller

## ESP-EYE v2.1 specifics

ESP-EYE specifications can be found [here](https://www.mouser.de/ProductDetail/Espressif-Systems/ESP-EYE?qs=l7cgNqFNU1iWrlpTZmwCRA%3D%3D).

## Requirements

**Model deployment**

Once a model has been generated, the C-array encoded model under `bin_model/model_hexgraph.cc` must be added to the embedded code.

Ensure you are in the project root folder.

    cd path/to/project

Copy the model. This will override the previous model.

    python3 src/tf_lite_model/model_to_mcu.py

**No model**

See these [instructions](README.md).

## Running a model for inference

You can compile the model using the VSCode ESP-IDF commands.
For example with "ESP-IDF: Build, Flash and start a monitor on your device".

Alternatively you can add the compile command to your path to build from the terminal.

    gedit ~/.bashrc

At the end of the file append the following.

    alias get_idf='. $HOME/esp/esp-idf/export.sh'

To start building navigate to the deployment directory.

    cd path/to/src/tinyml_deployment

You need to generate the build instructions once.

    get_idf

Set target.

    idf.py set-target esp32

You may want to list available targets

    idf.py --list-targets

Configure settings.

    idf.py menuconfig
    # choose menu point camera pins
    # for ESP-EYE v2.1 select ESP_EYE DevKit

    # TODO: this information is incomplete
    # image capturing doesn't work with above settings
    # we fixed this by copying the `sdkconfig` file from an old example
    # https://blog.tensorflow.org/2020/08/announcing-tensorflow-lite-micro-esp32.html
    # we don't know which setting is relevant
    # diff between our generated sdkconfig and the working file has more than 200 lines 

To build, run the following.

    idf.py build

Flash to device and open serial monitor.

    # note, you may need to change the usb device
    idf.py -p /dev/ttyUSB0 flash monitor

    # for more fine grained control the following also works for flashing
    esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash --flash_mode dio --flash_size 4MB --flash_freq 40m 0x1000 build/bootloader/bootloader.bin 0x8000 build/partition_table/partition-table.bin 0x10000 build/Rock_Paper_Scissors.bin

For convenience.

    cd src/tinyml_deployment && get_idf && idf.py build && idf.py -p /dev/ttyUSB0 flash monitor

For diagnostics, you can get memory info. Run after `build` but before flashing.

    idf.py size # basic information
    idf.py size-components # detailed info

## Submodules for dependency management

Add a new submodule.

        git submodule add https://remote/source
        # make a commit after adding a submodule
        git add .
        git commit -m "added submodule"
    
Remove a submodule.

        # simple remove
        git rm path/to/submodule
        # purge from history
        rm -rf .git/modules/path-to-submodule
        git config --remove-section submodule.path-to-submodule

## Memory limitation

Static memory allocation is limited to less than 160 kB on ESP32 based MCUs such as the ESP-EYE v2.1, as documented [here](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/mem_alloc.html).
Before any model inference takes place we initialize memory in the `tensor_arena`.
TFLite Micro expects static memory allocation for `tensor_arena`.
The combination of ESP32 and TFLite is therefore not ideal for larger models, see [this issue](https://github.com/espressif/tflite-micro-esp-examples/issues/3).
Due to the limitations, the `kTensorArenaSize` should not exceed around $150 \cdot 1024$ bytes in the following code snippet.

    constexpr int kTensorArenaSize = 150 * 1024;
    alignas(16) uint8_t tensor_arena[kTensorArenaSize];

Working with image data we have $x$ and $y$ dimensions and 3 color channels. We also must consider the data type of each pixel.

$\text{required memory} = x \cdot y \cdot \text{channels} \cdot \text{bytes}_\text{dtype}$

For example take an image with 240 $\times$ 240 and `int32` pixels. An `int32` takes up 4 bytes of memory.

$\text{memory} = 240 \cdot 240 \cdot 3 \cdot 4 = 691200 \text{ bytes}$

Reducing the image size to 96 $\times$ 96 yields.

$\text{memory} = 96 \cdot 96 \cdot 3 \cdot 4 = 110592 \text{ bytes}$

We can also use `uint8` types to represent 0 to 255, which is the range of pixel intensities, with one byte.

$\text{memory} = 96 \cdot 96 \cdot 3 \cdot 1 = 27648 \text{ bytes}$

Ensure to pass the `tensorflow` task a memory amount somewhat larger than the size of `tensor_arena`.
For example we have $120 \cdot 1024$ for `tensorflow` and $115 \cdot 1024$ for `tensor_arena`.

    extern "C" void app_main() {
        xTaskCreate((TaskFunction_t)&tf_main, "tensorflow", 120 * 1024, NULL, 8, NULL);
        vTaskDelete(NULL);
    }

## Limited support between TensorFlow and TfLite Micro

Not all Tensorflow Models are supported by TfLite.
And not all TfLite models are supported by TfLite Micro.
Find a list of supported TfLite Micro operations, [here](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/all_ops_resolver.cc).

The tensorflow modules that are used in the model architecture must be imported from tflite.
For example we may have used [ResNet50](https://github.com/keras-team/keras-applications/blob/master/keras_applications/resnet50.py).
Manually inspect the source code.

Add the header.

    #include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

Add the number of imports.

    static tflite::MicroMutableOpResolver<your number of imports> micro_op_resolver;

Add the imports. For example a dense layer is the built in operator fully connected.

    micro_op_resolver.AddBuiltin(
        tflite::BuiltinOperator_FULLY_CONNECTED,
        tflite::ops::micro::Register_FULLY_CONNECTED());

If this fails you may wish to import all modules.
Include a different resolver.

    #include "tensorflow/lite/micro/all_ops_resolver.h"

And declare it differently, too.    

    static tflite::ops::micro::AllOpsResolver resolver;

Note, not all layers in TF exist in TfLite Micro, therefore not all architectures will work.
Check the [source code](https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/all_ops_resolver.cc) to see which layers are available.
It's still not as simple as that.
For example, dropout cannot be found in the layers but still works because it's just a weight manipulation within possibly existing layers.
