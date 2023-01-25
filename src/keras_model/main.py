from model_custom import make_model_custom
from model_mobile import make_model_mobile
from model_resnet50 import make_model_resnet50
from dataset import train_ds, test_ds, INPUT_IMG_SHAPE, BATCH_SIZE
import importlib.util
import sys

import argparse
from pathlib import Path

from tensorflow import keras

# define constants
NUM_CLASSES = len(train_ds.class_names)
MODEL_PATH = Path("bin_model")
MODEL_PATH.mkdir(exist_ok=True)
EPOCHS = 10

# init command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, choices=["mobile", "resnet50",
    "simple-dense", "simple-cnn", "optimized-cnn"],
    default="optimized-cnn", help="select a model type")
parser.add_argument("--early", action='store_true', help="enable early stopping")
parser.add_argument("--step_save", action='store_true', help="save after each training epoch")
args = parser.parse_args()

# load and prefetch datasets
train_ds = train_ds.prefetch(buffer_size=32)
test_ds = test_ds.prefetch(buffer_size=32)

def main():
    # initialize model
    model = None
    if args.model == "mobile":
        print("MobileNetV2 model.")
        model = make_model_mobile(INPUT_IMG_SHAPE)
    if args.model == "resnet50":
        print("ResNet50 model.")
        model = make_model_resnet50(INPUT_IMG_SHAPE)
    if args.model == "simple-dense":
        print("Custom simple-dense model.")
        model = make_model_custom(INPUT_IMG_SHAPE, NUM_CLASSES, args.model)
    if args.model == "simple-cnn":
        print("Custom simple-cnn model.")
        model = make_model_custom(INPUT_IMG_SHAPE, NUM_CLASSES, args.model)
    if args.model == "optimized-cnn":
        print("Custom optimized-cnn model.")
        model = make_model_custom(INPUT_IMG_SHAPE, NUM_CLASSES, args.model)
    try:
        keras.utils.plot_model(model, show_shapes=True, to_file=MODEL_PATH / "model.png")
    except:
        print("Proceeding without plotting model.")

    # define callbacks
    callbacks = []
    if args.step_save == True:
        print("Saving after each epoch.")
        callbacks.append(
            keras.callbacks.ModelCheckpoint(
                filepath=MODEL_PATH / "save_at_epoch{epoch}.h5",
                save_weights_only=True,
                verbose=1,
            )
        )
    if args.early == True:
        print("Early Stopping.")
        callbacks.append(
            keras.callbacks.EarlyStopping(
                patience=3,
                mode="max",
            )
        )

    # compile model
    model.compile(
        optimizer=keras.optimizers.SGD(0.06),
        #optimizer=keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
        run_eagerly=True, # this may reduce performance but allows tensor.numpy()
    )

    # train model
    model.fit(
        train_ds, epochs=EPOCHS, callbacks=callbacks, validation_data=test_ds,
    )

    # save fully trained model
    model.save(MODEL_PATH / "keras_model")

main()