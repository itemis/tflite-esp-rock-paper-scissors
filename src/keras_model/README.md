# Keras Model

## Running

Set your path to the project root folder.

    cd path/to/project

Ensure you have train and test data in place.

    tree data/

If desired, consider whether data augmentation has been applied.

    # see src/data_augmentation for more information
    # some data augmentation may additionally be defined within the tensorflow model definition

Train the model.

    python src/keras_model/main.py
    # the model is saved under bin_model/keras_model

## Models

Currently two models have been implemented.
Firstly, an architecture defined by F. Chollet which is trained from scratch.
Second, a MobileNetV2 architecture that is pre-trained on the imagent dataset.
For MobileNetV2 only the output layer is trained, thus speeding up the process; this is known as transfer learning.