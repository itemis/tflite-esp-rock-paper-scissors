This is a Python wrapper of the
[imagemorph](https://github.com/GrHound/imagemorph.c) repository by Lambert
Schomaker (see last section). Rather than running a compiled executable and
writing the resulting image to disk as in the original repo, the `imagemorph.py` 
module provides a Python wrapper function which performs the same random elastic 
morphing as in the original repo, but instead returns the resulting image as
a numpy array, which can then be used for further processing in, for example,
a machine learning pipeline.

Any image type can be processed (not just .ppm), as long as it can be
loaded with OpenCV.

The code was tested on Ubuntu 16.04, using Python 3.6.

## Required packages

Running the Python script requires `numpy` and `opencv`, which can be installed
with pip:

```
pip install numpy opencv-python
```

## How to run

First build and link the C library:

```
python setup.py build
```

This will create a `build` folder, which contains the shared library that is
required for running the `imagemorph.py` module. Make sure not to move the
library anywhere above `imagemorph.py` in the file tree, otherwise it will not
be found and the code will not run. 

For a demo of the module, run

```
python imagemorph.py
```

which will apply the random elastic morphing to the `sampled-input.png` image
and save the result to `img/out.png`.

## Importing the imagemorph module into your code

If you want to use the elastic morphing in your own Python code, first clone
this repository to the same location as your Python code. You can then import 
the module in your code:

```python
from imagemorph.imagemorph import elastic_morphing
```

Alternatively, if you want to store this repository in some other location, you
can also make a symbolic link at the location where you want to import the
module:

```
cd path/to/your/code
ln -s imagemorph /path/to/imagemorph/folder
```

This will create a shortcut called `imagemorph` in the `path/to/your/code`
directory, which points to the imagemorph repo at `path/to/imagemorph/folder`.
You can then import the module as mentioned above.

# imagemorph.c
Program to apply random elastic rubbersheet  transforms to Netpbm color (.ppm) images for  augmenting training sets in machine learning/deep learning.  The program reads an input .ppm image from stdin and writes a ppm image to stdout.  Original Author: Marius Bulacu (.pgm version for characters). Adapted for .ppm and color: Lambert Schomaker

Please cite:

M Bulacu, A Brink, T van der Zant, L Schomaker (2009).
Recognition of handwritten numerical fields in a 
large single-writer historical collection,
10th International Conference on Document Analysis and Recognition, 
pp. 808-812, DOI: 10.1109/ICDAR.2009.8 
