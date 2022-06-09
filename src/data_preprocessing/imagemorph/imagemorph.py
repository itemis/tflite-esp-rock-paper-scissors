import sys
from ctypes import cast, CDLL, c_double, c_int, POINTER, Structure
from pathlib import Path

import cv2 as cv
import numpy as np


class Pixel(Structure):
    """This class mimics the Pixel structure defined in imagemorph.c."""

    _fields_ = [("r", c_int), ("g", c_int), ("b", c_int)]


def elastic_morphing(img, amp, sigma, h, w):
    """Apply random elastic morphing to an image.

    Args:
        img: BGR image in the form of a numpy array of shape (h, w, 3).
        amp: average amplitude of the displacement field (average pixel displacement)
        sigma: standard deviation of the Gaussian smoothing kernel
        h: height of the image
        w: width of the image
    """
    assert img.shape == (h, w, 3), f"img should have shape (h, w, 3), not {img.shape}"

    # load C library
    try:
        cwd = Path(__file__).resolve().parent  # location of this module
        libfile = list(cwd.rglob("libimagemorph*.so"))[0]
    except IndexError:
        print(
            "Error: imagemorph library could not be found. Make sure to "
            "first compile the C library using `python setup.py build`."
        )
        sys.exit()

    c_lib = CDLL(libfile)

    # load the elastic morphing function from the C library
    elastic_morphing = c_lib.elastic_morphing
    elastic_morphing.restype = POINTER(POINTER(Pixel))
    elastic_morphing.argtypes = [
        POINTER(POINTER(Pixel)),
        c_int,
        c_int,
        c_double,
        c_double,
    ]

    # convert parameters to C compatible data types
    img_c = (h * POINTER(Pixel))()
    for i in range(h):
        row = (w * Pixel)()
        for j in range(w):
            b, g, r = img[i, j]
            row[j] = Pixel(r, g, b)
        img_c[i] = cast(row, POINTER(Pixel))
    img_c = cast(img_c, POINTER(POINTER(Pixel)))
    amp_c, sigma_c = c_double(amp), c_double(sigma)
    h_c, w_c = c_int(h), c_int(w)

    # apply the elastic morphing to the image
    img_c = elastic_morphing(img_c, h_c, w_c, amp_c, sigma_c)

    # convert the result to a numpy array
    res = np.zeros_like(img)
    for i in range(h):
        for j in range(w):
            px = img_c[i][j]
            res[i, j] = [px.b, px.g, px.r]
    return res


if __name__ == "__main__":
    amp, sigma = 0.9, 9
    img_name = "img/sample-input.png"

    # load image
    img = cv.imread(img_name)
    h, w, _ = img.shape

    # apply elastic morphing
    res = elastic_morphing(img, amp, sigma, h, w)

    # write result to disk
    cv.imwrite("img/out.png", res)
