from pathlib import Path
import shutil

# TODO: cmdline arg
DATA_PATH = Path("data/raw_images")

assert DATA_PATH.exists(), "The path to your train data does not exist!"

def balance_classes():
    """Let all classes have same number of examples."""

    # get directory names
    dirs = [file for file in DATA_PATH.iterdir() if file.is_dir()]

    # number of files in dir with least files
    min_files = min([len(list(dir.iterdir())) for dir in dirs])

    for dir in dirs:
        # make new folders for each dir
        new_name = dir.name + "_reduced"
        new_dir = DATA_PATH / new_name
        new_dir.mkdir(exist_ok=True)
        # get all files in dir
        files = list(dir.iterdir())
        counter = 0
        for f in files:
            # skip images where a class has more than the class with least images.
            if counter >= min_files: break
            
            shutil.copyfile(f, new_dir / f.name)
            counter += 1

balance_classes()

