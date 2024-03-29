from pathlib import Path
from augmentation_layers import Dilate

from pathlib import Path

import cv2 as cv
import numpy as np
import tensorflow as tf
from keras import layers


from imagemorph.imagemorph import elastic_morphing

DEBUG = False

class Augmentor:
    """Applies data augmentation directly to training data and writes to file."""

    def __init__(self) -> None:
        """Initialize the augmenter."""
        pass

    def erosion_image(self, img_path: Path,
        min_kernel_size: int=3, max_kernel_size: int=3) -> None:
        """Erode the image at the given path."""
        original = cv.imread(str(img_path))
        for i in range(min_kernel_size, max_kernel_size + 1):
            kernel = np.ones((i, i), np.uint8)
            eroded_img = cv.erode(original, kernel, iterations=1)
            # e for eroded
            # i for the kernel size
            # parents[0] gives the path to the current file
            # stem gives the file name without the extension
            new_path = img_path.parent / (str(img_path.stem) + "e" + str(i) + ".jpg")
            if DEBUG:
                cv.imshow("eroded", eroded_img)
            else:
                cv.imwrite(str(new_path), eroded_img)

    def dilate_image(self, img_path: Path,
        min_kernel_size: int=3, max_kernel_size: int=3) -> None:
        """Dilate the image at the given path."""
        original = cv.imread(str(img_path))
        
        for i in range(min_kernel_size, max_kernel_size + 1):
            kernel = np.ones((i, i), np.uint8)
            dilated_img = cv.dilate(original, kernel, iterations=1)
            # d for dilated
            # i for the kernel size
            # parents[0] gives the path to the current file
            # stem gives the file name without the extension
            new_path = img_path.parent / (str(img_path.stem) + "d" + str(i) + ".jpg")
            if DEBUG:
                cv.imshow("dilated", dilated_img)
            else:
                cv.imwrite(str(new_path), dilated_img)

    def elastic_morph_wrapper(self, img_path: Path,
        amp: float=0.5, sigma: float=0.5, reps: int=1) -> None:
        """Morphing the image at the given path."""
        # amp is the amplitude of the deformation
        # sigma is the local image area affected (spread of the gaussian smoothing kernel)
        original = cv.imread(str(img_path))
        h, w, _ = original.shape  # image height and width

        # repeat the morphing `reps` times
        for rep in range(reps):
            res = elastic_morphing(original, amp, sigma, h, w)  # morph image
            # m for morphed
            # i for the kernel size
            # parents gives the parent to the current file
            # stem gives the file name without the extension
            new_path = img_path.parent / (str(img_path.stem) + "m" + str(rep) + ".jpg")
            if DEBUG:
                cv.imshow("morphed", res)
            else:
                cv.imwrite(str(new_path), res)

    def euclidian_transform(self, img_path: Path,
        rotation: int=20, reps: int=1) -> None:
        """Euclidean transform the image at the given path."""
        original = cv.imread(str(img_path))
        rows,cols,_ = original.shape

        for rep in range(reps):
            # rotation
            theta = np.random.randint(-rotation, rotation+1)
            M_r = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),theta,1)
            distorted = cv.warpAffine(original, M_r, (cols, rows))

            # translation
            t_x = np.random.randint(-cols//10, cols//10+1)
            t_y = np.random.randint(-rows//10, rows//10+1)
            M_t = np.float32([[1, 0, t_x], [0, 1, t_y]])
            distorted = cv.warpAffine(distorted, M_t, (cols, rows))

            # save
            new_path = img_path.parent / (str(img_path.stem) + f"theta{theta}"
                + f"tx{t_x}" + f"ty{t_y}" + f"rep{rep}" + ".jpg")
            if DEBUG:
                cv.imshow("euclidean transform", distorted)
            else:
                cv.imwrite(str(new_path), distorted)

    def keras_layers(self, img_path: Path, reps: int = 1):
        """
        One or multiple keras augmentation layers.
        Quite slow.
        """
        # BUG: file-wide import of matplotlib causes OpenCV to crash
        import matplotlib.pyplot as plt
        
        # load image and convert to tensorflow format
        im = plt.imread(str(img_path))
        im = tf.cast(tf.expand_dims(im, 0), tf.float32)

        # define augmentation layers
        augment_layers = tf.keras.Sequential([
            # TODO: custom Dilate layer is very slow
            # Dilate(kernel_min=0, kernel_max=3),
            layers.RandomRotation(factor=[-0.1, 0.1]),
            layers.RandomContrast(factor=0.4),
            # TODO: can't find RandomBrightness in tf.keras.layers, tensorflow version 2.9.1
            # layers.RandomBrightness(factor=[0.1, 0.2]),
            layers.RandomZoom(height_factor=(-0.02, 0.2), width_factor=(-0.02, 0.2)),
        ])
        
        for i in range(reps): # number of augmentations per image
            augmented_image = augment_layers(im)
            
            new_path = img_path.parent / (str(img_path.stem) + "keras" + str(i) + ".jpg")
            
            if DEBUG:
                fig = plt.figure(frameon=False)
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.imshow(augmented_image[0])
                plt.show()
            # TODO: implement saving in grayscale and correct resolution
            # plt.savefig(new_path, cmap='gray')

    def check_image_morphing_setup(self) -> bool:
        """Check if the image morphing setup is correct."""
        current_file_path = Path(__file__).parent.resolve()
        if (current_file_path / "build").exists():
            return True
        else:
            print("Image morphing has not been built.")
            return False

    def apply_all_augmentation(self, train_dir: Path):
        """Apply all augmentation methods to the image at the given path.
        
        args:
            train_dir: path to the training data directory
        """
        class_list = [dir for dir in train_dir.iterdir() if dir.is_dir()]
        for cls in class_list:
            images = [im for im in cls.iterdir() if im.is_file()]
            print(images)
            for im in images:
                print(f"Augmenting {str(im)}")
                self.dilate_image(im)
                self.erosion_image(im)
                if self.check_image_morphing_setup():
                    self.elastic_morph_wrapper(im)
                self.euclidian_transform(im)
                self.keras_layers(im)

if __name__ == "__main__":
    pass
