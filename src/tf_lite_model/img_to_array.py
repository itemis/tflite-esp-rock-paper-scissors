from pathlib import Path
import cv2
import numpy as np

IMG_PATH = Path("data/scissors.jpg")

FOOTER = "};\n"

def get_cfile_header(file_name: str) -> str:
    return (
"""#include <stdint.h>
uint8_t """ + file_name + "[] = { \n"
)

def convert_rgb(IMG_PATH):
    """Load an RGB image and convert it to a static C-array."""
    # RBG images with 3 channels
    im = cv2.imread(str(IMG_PATH))
    b,g,r = cv2.split(im)
    im_li = [b,g,r]

    channel_name=["b_channel", "g_channel", "r_channel"]
    for name, img in zip(channel_name, im_li):
        header = get_cfile_header(name)
        np.savetxt("data/" + name, img, fmt="%i", delimiter=",", newline=',\n', coments="", header=header, footer=FOOTER)

def convert_gray(IMG_PATH):
    """Load a grayscale image and convert it to a static C-array.
    
    BUG: The newline character is added to the end of the header and footer and needs to be manually removed. 
    This could be considered an error in numpy.savetxt().
    """
    var_name = "grayscale"
    file_name = var_name + ".cc"
    header = get_cfile_header(var_name)
    im = cv2.imread(str(IMG_PATH), cv2.IMREAD_GRAYSCALE)
    np.savetxt("data/" + file_name, im, fmt="%i", delimiter=",", newline=',\n', comments="", header=header, footer=FOOTER)

convert_gray(IMG_PATH)