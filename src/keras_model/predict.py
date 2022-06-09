from dataset import train_ds

from pathlib import Path

import tensorflow as tf
import cv2 as cv
from tensorflow import keras
import numpy as np

MODEL_PATH = Path("bin_model") / "keras_model"

def predict_image(model, im: Path, labels: list) -> None:
    """predict class label for a single image."""
    img = cv.imread(str(im), cv.IMREAD_GRAYSCALE)

    # NOTE: add dim 1 in front because TF 
    img = tf.expand_dims(img, axis=0) 
    preds = model.predict(img, verbose=1)

    # paper, rock, scissors
    print("Prediction vector:")
    print(labels)
    print(preds)
    print("Predicted class:")
    class_index = np.argmax(preds)
    print(f"class: {class_index}, {labels[class_index]}")

def main():
    """do some test predictions."""
    labels = train_ds.class_names
    model = keras.models.load_model(str(MODEL_PATH))
    test_im_names = ["rock.png", "paper.png", "scissors.png"]
    train_im_names = ["rock_train.png", "paper_train.png", "scissors_train.png"]
    hardcore_im_names = ["rock_with_head.jpg", "paper_with_head.jpg", "scissors_with_head.jpg"] 
    for im in hardcore_im_names:
        im_path = Path("data") / im
        predict_image(model, im_path, labels)

