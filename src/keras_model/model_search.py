from tensorflow import keras

def make_model_cnn_search(hp, INPUT_IMG_SHAPE=(96, 96, 1), num_classes=3):
    model = keras.Sequential()
    model.add(keras.Input(shape=INPUT_IMG_SHAPE))
    rotation = hp.Float("rotation", min_value=0, max_value=0.2)
    model.add(keras.layers.RandomRotation(factor=[-rotation, rotation]))
    zoom_out = hp.Float("zoom_out", min_value=-0.1, max_value=0)
    zoom_in = hp.Float("zoom_in", min_value=0, max_value=0.1)
    model.add(keras.layers.RandomZoom(height_factor=(zoom_out, zoom_in), width_factor=(zoom_out, zoom_in)))
    model.add(keras.layers.Rescaling(1.0 / 255))

    # conv1
    model.add(keras.layers.Conv2D(
        filters=hp.Int("filters1", min_value=8, max_value=16, step=1),
        kernel_size=hp.Int("kernel_size1", min_value=1, max_value=5, step=1),
        strides=hp.Int("strides1", min_value=1, max_value=5, step=1),
        kernel_regularizer=keras.regularizers.L2(hp.Float("l2_kernel_1", min_value=0, max_value=1e-3)),
        bias_regularizer=keras.regularizers.L2(hp.Float("l2_bias_1", min_value=0, max_value=1e-3)),
        activity_regularizer=keras.regularizers.L2(hp.Float("l2_activ_1", min_value=0, max_value=1e-3)),
        padding="same"))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.Dropout(hp.Float("dropout1", min_value=0, max_value=1)))
    model.add(keras.layers.MaxPooling2D(padding="valid"))

    # conv2
    model.add(keras.layers.Conv2D(
        filters=hp.Int("filters2", min_value=8, max_value=16, step=1),
        kernel_size=hp.Int("kernel_size2", min_value=1, max_value=5, step=1),
        strides=hp.Int("strides2", min_value=1, max_value=5, step=1),
        kernel_regularizer=keras.regularizers.L2(hp.Float("l2_kernel_2", min_value=0, max_value=1e-3)),
        bias_regularizer=keras.regularizers.L2(hp.Float("l2_bias_2", min_value=0, max_value=1e-3)),
        activity_regularizer=keras.regularizers.L2(hp.Float("l2_activ_2", min_value=0, max_value=1e-3)),
        padding="same"))
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.Dropout(hp.Float("dropout2", min_value=0, max_value=1)))
    model.add(keras.layers.MaxPooling2D(padding="valid"))

    # conv3
    model.add(keras.layers.Conv2D(
        filters=hp.Int("filters3", min_value=8, max_value=16, step=1),
        kernel_size=hp.Int("kernel_size3", min_value=1, max_value=5, step=1),
        strides=hp.Int("strides3", min_value=1, max_value=5, step=1),
        kernel_regularizer=keras.regularizers.L2(hp.Float("l2_kernel_3", min_value=0, max_value=1e-3)),
        bias_regularizer=keras.regularizers.L2(hp.Float("l2_bias_3", min_value=0, max_value=1e-3)),
        activity_regularizer=keras.regularizers.L2(hp.Float("l2_activ_3", min_value=0, max_value=1e-3)),
        padding="same"))
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.Dropout(hp.Float("dropout3", min_value=0, max_value=1)))
    model.add(keras.layers.MaxPooling2D(padding="same"))

    # flatten
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(hp.Float("dropout4", min_value=0, max_value=1)))
    
    # dense
    units=hp.Int("units", min_value=0, max_value=16, step=1)
    dropout5 = hp.Float("dropout5", min_value=0, max_value=1)
    l2_kernel_5 = hp.Float("l2_kernel_5", min_value=0, max_value=1e-3)
    l2_bias_5 = hp.Float("l2_bias_5", min_value=0, max_value=1e-3)
    l2_activ_5 = hp.Float("l2_activ_5", min_value=0, max_value=1e-3)
    if units > 0:
        model.add(keras.layers.Dense(
            units=units,
            kernel_regularizer = keras.regularizers.L2(l2_kernel_5),
            bias_regularizer = keras.regularizers.L2(l2_bias_5),
            activity_regularizer = keras.regularizers.L2(l2_activ_5),
            activation="relu"))
        model.add(keras.layers.Dropout(dropout5))
    
    # read out
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes
    model.add(keras.layers.Dense(units, activation=activation))

    sgd_learning_rate = hp.Float("sgd_learning_rate", min_value=1e-3, max_value=1e-1)
    adam_learning_rate = hp.Float("adam_learning_rate", min_value=1e-4, max_value=1e-2)
    opt = keras.optimizers.SGD(learning_rate=sgd_learning_rate)
    opt_choice = hp.Choice("optimizer", ["adam", "sgd"])
    if opt_choice == "adam":
        opt = keras.optimizers.Adam(learning_rate=adam_learning_rate)
    model.compile(
        optimizer=opt,
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model

make_model = make_model_cnn_search