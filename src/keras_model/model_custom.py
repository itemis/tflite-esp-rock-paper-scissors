import tensorflow as tf
from tensorflow import keras
from keras import layers

# TODO: Keras preprocessing and Keras data augmentation is convenient
# can we use it together with the MCU?

def make_model_simple_dense(INPUT_IMG_SHAPE, num_classes=3):
    inputs = keras.Input(shape=INPUT_IMG_SHAPE)
    x = inputs

    # preprocessing
    x = layers.Rescaling(1.0 / 255)(x)

    x = layers.MaxPooling2D(pool_size=(8, 8))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(4)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(2)(x)

    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    #x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

def make_model_simple_cnn(INPUT_IMG_SHAPE, num_classes=3):
    inputs = keras.Input(shape=INPUT_IMG_SHAPE)
    x = inputs

    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(16, 3, strides=3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(32, 3, strides=2, padding='same', activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, padding='same', activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Flatten()(x)
    x = layers.Dropout(0.5)(x)

    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

def make_model_optimized_cnn(INPUT_IMG_SHAPE, num_classes=3):
    """
    A note on regularization.
    Dropout seems too invasive for such a small network.
    L1 and L2 regularization and data augmentation seem preferable.

    Optimizer: SGD
    Learning Rate: 0.06
    Epochs: 10
    """
    inputs = keras.Input(shape=INPUT_IMG_SHAPE)
    x = inputs

    # preprocessing and augmentation
    x = layers.RandomRotation(factor=[-0.05, 0.05])(x)
    #x = layers.RandomContrast(factor=0.4)(x) # NOTE: slow and throws warning
    #x = layers.RandomBrightness(factor=[0.1, 0.2])(x) # NOTE: slow and throws warning
    x = layers.RandomZoom(height_factor=(-0.01, 0.1), width_factor=(-0.01, 0.1))(x)
    x = layers.Rescaling(1.0 / 255)(x)

    # conv1
    x = layers.Conv2D(filters=12, kernel_size=5, strides=3, padding="same",
        kernel_regularizer=keras.regularizers.L1L2(l1=1e-5, l2=1e-4),
        bias_regularizer=keras.regularizers.L2(1e-4),
        activity_regularizer=keras.regularizers.L2(1e-5),
        )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D(padding="valid")(x)

    # conv2
    x = layers.Conv2D(filters=12, kernel_size=5, strides=3, padding="same",
        kernel_regularizer=keras.regularizers.L1L2(l1=1e-5, l2=1e-4),
        bias_regularizer=keras.regularizers.L2(1e-4),
        activity_regularizer=keras.regularizers.L2(1e-5),
    )(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D(padding="valid")(x)

    # conv3
    x = layers.Conv2D(filters=15, kernel_size=2, strides=1, padding="same",
        kernel_regularizer=keras.regularizers.L1L2(l1=1e-5, l2=1e-4),
        bias_regularizer=keras.regularizers.L2(1e-4),
        activity_regularizer=keras.regularizers.L2(1e-5),
    )(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D(padding="valid")(x)

    # flatten
    x = layers.Flatten()(x)

    # dense
    x = layers.Dense(units=9, activation="relu",
        kernel_regularizer=keras.regularizers.L1L2(l1=1e-5, l2=1e-4),
        bias_regularizer=keras.regularizers.L2(1e-4),
        activity_regularizer=keras.regularizers.L2(1e-5),
    )(x)

    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

def make_model_custom(INPUT_IMG_SHAPE, model_type):
    if model_type == "simple-dense":
        return make_model_simple_dense(INPUT_IMG_SHAPE)
    if model_type == "simple-cnn":
        return make_model_simple_cnn(INPUT_IMG_SHAPE)
    if model_type == "optimized-cnn":
        return make_model_optimized_cnn(INPUT_IMG_SHAPE)
    else:
        print("UNKOWN MODEL DEFINITION.")