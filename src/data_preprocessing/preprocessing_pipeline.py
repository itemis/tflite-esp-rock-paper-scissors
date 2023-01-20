import argparse

import const
import preprocess
import balance_classes
import split_data
import augment

parser = argparse.ArgumentParser(
                    prog = "Image Preprocessing Pipeline",
                    description = "Resize, crop, grayscale, balance classes, and split data into train and test sets",
                    epilog = "Nikolas Rieder, Rafael Tappe Maestro, Itemis AG, 2022")
parser.add_argument("-a", "--augment",
                    action="store_true")  # on/off flag
args = parser.parse_args()

def main(args):
    # shrink, crop, grayscale the images
    preprocess.apply_over_set(const.CLASS_LIST)
    print("")
    balance_classes.balance_classes_in_place(const.CLASS_LIST)
    print("")
    split_data.split_data(const.CLASS_LIST, const.TRAIN_PATH, const.TEST_PATH)
    print("")
    if args.augment:
        augmentor = augment.Augmentor()
        augmentor.apply_all_augmentation(const.TRAIN_PATH)

if __name__ == "__main__":
    main(args)