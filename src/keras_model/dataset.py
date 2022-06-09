from pathlib import Path
import tensorflow as tf

DATA_ROOT = Path("data")

BATCH_SIZE=32
IMG_WIDTH_HEIGHT=(96, 96)
IMG_CHANNELS = 1
INPUT_IMG_SHAPE=IMG_WIDTH_HEIGHT + (IMG_CHANNELS,)

train_ds = tf.keras.utils.image_dataset_from_directory(
    directory= DATA_ROOT / "train",
    labels='inferred',
    label_mode='categorical',
    batch_size=BATCH_SIZE,
    image_size=IMG_WIDTH_HEIGHT,
    color_mode='grayscale',
    )
test_ds = tf.keras.utils.image_dataset_from_directory(
    directory= DATA_ROOT / "test",
    labels='inferred',
    label_mode='categorical',
    batch_size=BATCH_SIZE,
    image_size=IMG_WIDTH_HEIGHT,
    color_mode='grayscale'
    )
hard_ds = tf.keras.utils.image_dataset_from_directory(
    directory= DATA_ROOT / "hard",
    labels='inferred',
    label_mode='categorical',
    batch_size=BATCH_SIZE,
    image_size=IMG_WIDTH_HEIGHT,
    color_mode='grayscale'
    )