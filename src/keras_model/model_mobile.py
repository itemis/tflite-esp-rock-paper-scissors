from tensorflow import keras

def make_model_mobile(INPUT_IMG_SHAPE):
    
    """
    Use transfer learning to accelerate training.
    Base model is trained on imagenet data set.
    The base model has learnt feature extraction.
    The base model is frozen, hence not trained.
    A fully connected layer is added at the end.
    Only this layer is trained.

    See reference https://towardsdatascience.com/transfer-learning-rock-paper-scissors-classifier-45a148224da9
    """
    base_model = keras.applications.MobileNetV2(
        input_shape=INPUT_IMG_SHAPE,
        include_top=False, # last fully connected layer is removed
        pooling='avg' # global pooling, in_dim=n out_dim=1, like flatten
    )

    # freeze the base model
    base_model.trainable = False

    model = keras.models.Sequential()

    model.add(base_model) # frozen base model
    # drouput sets weights randomly to 0
    model.add(keras.layers.Dropout(0.5))
    # fully connected output layer
    model.add(keras.layers.Dense(
        units=3,
        activation=keras.activations.softmax
    ))

    return model
