from pathlib import Path

TARGET_DIM = (96, 96)

DATA_PATH = Path("data")
RAW_DATA_PATH = Path("data") / "raw_images"
assert DATA_PATH.exists(), "The path to your train data does not exist!"
# list of classes, as given by the folder names
CLASS_LIST = [dir for dir in RAW_DATA_PATH.iterdir() if dir.is_dir()]
# train-test split, 0.8 corresponds to 80% of images
TRAIN_FRAC = 0.8
TEST_FRAC = 1-TRAIN_FRAC 

TEST_PATH = DATA_PATH / "test"
TRAIN_PATH = DATA_PATH / "train"