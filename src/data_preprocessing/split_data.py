import random
import shutil
from pathlib import Path
from typing import List

import const

random.seed(1)

def split_data(class_dirs: List[Path], train_path: Path, test_path: Path) -> None:
    """split data into train and test set.
    
    args:
        class_dirs: list of paths to class directories containing images
        test_path: path to write the test directory
        train_path: path to write the train directory
    """
    print("Splitting data into train and test set...")
    test_path.mkdir(exist_ok=True, parents=True)
    train_path.mkdir(exist_ok=True, parents=True)

    # iterate the class directories
    for dir in class_dirs:
        # skip non existing directories
        if not dir.is_dir(): continue
        # number of files in a directory
        files = list(dir.iterdir())
        # num files for training and testing
        num_files = len(files)
        num_train = int(num_files * const.TRAIN_FRAC)
        # shuffle files
        random.shuffle(files)
        # select train and test files
        train_files = files[:num_train]
        test_files = files[num_train:]
        # copy files
        for f in train_files:
            new_dir = train_path / dir.name
            new_dir.mkdir(exist_ok=True, parents=True)
            shutil.copyfile(f, new_dir / f.name)
        for f in test_files:
            new_dir = test_path / dir.name
            new_dir.mkdir(exist_ok=True, parents=True)
            shutil.copyfile(f, new_dir / f.name)

if __name__ == "__main__":
    pass