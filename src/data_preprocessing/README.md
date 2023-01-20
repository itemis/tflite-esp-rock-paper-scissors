# Data Augmentation

## Requirements

The purpose of files in the folder is to produce data of the correct format, looking as follows.

    cd path/to/project

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

Raw images should be placed into the location

    path/to/project/data/raw_images/class_name/

Where `class_name` may for example be rock, paper or scissors.
In order to apply basic preprocessing without data augmentation, run

    python src/data_preprocessing/preprocessing_pipeline.py

This will

1. resize
2. crop
3. convert to grayscale
4. balance classes
5. split images into train and test sets

A test and train set will be produced at `data/train` and `data/test` respectively.

### Data Augmentation

Build C library for imagemorph augmentation.

    cd path/to/data_augmentation/image_morph
    python setup.py build

Your path of execution for augmentation must be the project root folder.

    cd path/to/tflite-es32-eye-paper-stone-scissors
    python src/data_augmentation/augment.py

To run the preprocessing pipeline with data augmentation add flag `-a`

    python src/data_preprocessing/preprocessing_pipeline.py -a

The augmented images will be writen to `data/train`.