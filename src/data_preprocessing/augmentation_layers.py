
import cv2 as cv
import numpy as np
import tensorflow as tf

DEBUG = True

def tf_to_cv(t: tf.Tensor) -> np.ndarray:
    t = t.numpy()
    return t

def cv_to_tf(arr: np.ndarray) -> tf.Tensor:
    arr = tf.convert_to_tensor(arr)
    arr = tf.expand_dims(arr, axis=arr.ndim)
    return arr 

class Dilate(tf.keras.layers.Layer):
    """
    Dilate image with random kernels.
    Layer for TensorFlow models.
    Implementation is slow and needs optimization.
    """

    def __init__(self, kernel_min=0, kernel_max=0):
        super().__init__()
        self.kernel_min = kernel_min
        self.kernel_max = kernel_max
        self.g = tf.random.Generator.from_non_deterministic_state()

    def get_rand_kernel_size(self):
        kernel_size = self.g.uniform(shape=[1],
            minval=self.kernel_min,
            maxval=self.kernel_max+1,
            dtype=tf.dtypes.int32)[0].numpy()
        return kernel_size

    def call(self, images: tf.Tensor, training=True):
        if training == False:
            return images
        
        kernel_size = self.get_rand_kernel_size()
        kernel = tf.ones((kernel_size, kernel_size), tf.dtypes.uint8).numpy()
        img_li = []
        for img in images: # receives batch of images
            img = tf_to_cv(img)
            img = cv.dilate(img, kernel, iterations=1)
            img = cv_to_tf(img)
            img_li.append(img)
        dilated_images = tf.stack(img_li)
        return dilated_images
