# Data Augmentation

## Requirements

To install required Python libraries run

    cd path/to/data_augmentation
    pip install -r requirements.txt

The data must be in the correct format.

    cd path/to/tflite-es32-eye-paper-stone-scissors

    data/
        train/
            rock/
                *.jpg
            paper/
                *.jpg
            scissors/
                *.jpg
        test/
            rock/
                *.jpg
            paper/
                *.jpg
            scissors/
                *.jpg

## Running

### Data Preprocessing

Crop train and test images to a target size.
The target size is set in the file `scale_crop.py`.

Your path of execution for augmentation must be the project root folder.

    cd path/to/tflite-es32-eye-paper-stone-scissors
    python src/data_augmentation/preprocess.py

### Data Augmentation

Build C library for imagemorph augmentation.

    cd path/to/data_augmentation/image_morph
    python setup.py build

Your path of execution for augmentation must be the project root folder.

    cd path/to/tflite-es32-eye-paper-stone-scissors
    python src/data_augmentation/augment.py

