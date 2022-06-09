import random
from pathlib import Path
import shutil

random.seed(1)

# path to folders with classes
# the folders should contain images
DATA_PATH = Path("data/raw_images")
assert DATA_PATH.exists(), "The path to your train data does not exist!"

# list of classes
# NOTE: folder's names and class names should be identical
CLASS_LIST = ["rock", "paper", "scissors"]

# train-test split, 0.8 corresponds to 80% of images
TRAIN_FRAC = 0.8
TEST_FRAC = 1-TRAIN_FRAC 

TEST_PATH = DATA_PATH / "test"
TRAIN_PATH = DATA_PATH / "train"

def split_data():
    """split data into train and test set."""
    TEST_PATH.mkdir(exist_ok=True)
    TRAIN_PATH.mkdir(exist_ok=True)
    dirs = [DATA_PATH / cls for cls in CLASS_LIST]

    # iterate the class directories
    for dir in dirs:
        # number of files in a directory
        num_files = len(list(dir.iterdir()))
        # num files for training and testing
        num_train = int(num_files * TRAIN_FRAC)
        # collect and shuffle files
        files = list(dir.iterdir())
        random.shuffle(files)
        # select train and test files
        train_files = files[:num_train]
        test_files = files[num_train:]
        # copy files
        for f in train_files:
            new_dir = DATA_PATH / "train" / dir.name
            new_dir.mkdir(exist_ok=True)
            shutil.copyfile(f, new_dir / f.name)
        for f in test_files:
            new_dir = DATA_PATH / "test" / dir.name
            new_dir.mkdir(exist_ok=True)
            shutil.copyfile(f, new_dir / f.name)

split_data()