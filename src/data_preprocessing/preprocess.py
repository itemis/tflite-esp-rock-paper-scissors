"""
Down or up-scale images and crop images to fit a target size.
Overrides original images.
"""

from pathlib import Path
from typing import List
import cv2
import numpy as np

import const

DEBUG = False

def rescale(im_path: Path) -> np.ndarray:
    """
    Take shortest side of the image and scale it to the target.
    Preserve aspect ratio.
    """
    img = cv2.imread(str(im_path))
    if DEBUG: cv2.imshow("img", img)

    dim = img.shape[0:2] # discard channels
    short_side = np.argmin(dim)

    scale = const.TARGET_DIM[short_side] / dim[short_side]
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    new_dim = (width, height)
    
    # resize by short side of image
    return cv2.resize(img, new_dim, interpolation = cv2.INTER_AREA)

def crop(img: np.ndarray = None, im_path: Path = None) -> np.ndarray:
    """
    Crop image to fit size of target image.
    Cropping is applied such that all sides are trimmed evenly.
    Function can take an image as numpy array as argument or a path.
    """
    # read image from file if path was specificed
    if im_path != None:
        img = cv2.imread(str(im_path))

    dim = img.shape
    x_diff = abs(dim[0] - const.TARGET_DIM[0])
    y_diff = abs(dim[1] - const.TARGET_DIM[1])
    x_half = x_diff // 2
    y_half = y_diff // 2

    # centered crop
    return img[0+x_half:dim[0]-x_half, 0+y_half:dim[1]-y_half]
        
def rgb_to_gray(img: np.ndarray = None, im_path: Path = None):
    """Convert image from RGB with 3 channels to grayscale with 1 channel."""
    
    # read image from file if path was specificed
    if im_path != None:
        img = cv2.imread(str(im_path))

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_over_set(class_dirs: List[Path]) -> None:
    """apply preprocessing to all images in the provided directories.

    args:
        class_dirs: list of paths to class directories containing images
    """
    for dir in class_dirs: # class folder names
        for im_path in dir.glob("**/*"):
            # TODO: im_path should point to an image
            print(f"Reshaping {str(im_path)}")
            im = rescale(im_path)
            if DEBUG: cv2.imshow("rescaled", im)
            im = crop(im)
            if DEBUG: cv2.imshow("cropped", im)
            im = rgb_to_gray(im)
            if DEBUG: cv2.imshow("gray", im)
            if DEBUG: cv2.waitKey(0)
            new_path = im_path.parents[0] / (str(im_path.name))
            cv2.imwrite(str(new_path), im)


if __name__ == "__main__":
    apply_over_set(const.DATA_PATH)
