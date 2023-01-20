from pathlib import Path
import shutil
from typing import List

def balance_classes_to_new_folder(dirs: List[Path]):
    """Let all classes have same number of examples.
    
    args:
        dirs: list of paths to class directories containing images
    """

    # number of files in dir with least files
    min_files = min([len(list(dir.iterdir())) for dir in dirs])

    for dir in dirs:
        # make new folders for each dir
        new_name = dir.name + "_reduced"
        new_dir = dir.parent / new_name
        new_dir.mkdir(exist_ok=True)
        # get all files in dir
        files = list(dir.iterdir())
        counter = 0
        for f in files:
            # skip images where a class has more than the class with least images.
            if counter >= min_files: break
            
            shutil.copyfile(f, new_dir / f.name)
            counter += 1
        # remove old dir
        shutil.rmtree(dir)
        # rename new dir
        new_dir.rename(dir.name)


def balance_classes_in_place(class_dirs: List[Path]):
    """Let all classes have same number of examples.
    
    args:
        class_dirs: list of paths to class directories containing images
    """
    print("Balancing classes in place...")

    # number of files in dir with least files
    min_files = min([len(list(dir.iterdir())) for dir in class_dirs if dir.is_dir()])

    for dir in class_dirs:
        files = list(dir.iterdir())
        counter = 0
        for f in files:
            if counter < min_files:
                counter += 1
                continue
            # remove files where a class has more than the class with least images.
            f.unlink()

if __name__ == "__main__":
    pass
