from model_search import make_model
from dataset import train_ds, test_ds, INPUT_IMG_SHAPE, BATCH_SIZE

from pathlib import Path

from tensorflow import keras
import keras_tuner

# define constants
MODEL_PATH = Path("bin_model")
assert MODEL_PATH.exists(), "The path to save your model does not exist!"

# load and prefetch datasets
train_ds = train_ds.prefetch(buffer_size=32)
test_ds = test_ds.prefetch(buffer_size=32)

def main():
    # define search paramaters
    tuner = keras_tuner.RandomSearch(
        make_model,
        objective='val_loss',
        max_trials=90,
        executions_per_trial=1,
        directory=MODEL_PATH,
        overwrite=True,
        project_name="hyppar_search",
    )
    print(tuner.search_space_summary())

    # perform hyperparameter search
    tuner.search(train_ds, epochs=5, validation_data=test_ds)
    print(tuner.results_summary())
    
    # choose best model
    model = tuner.get_best_models()[0]
    keras.utils.plot_model(model, show_shapes=True, to_file=MODEL_PATH / "model.png")
    print(model.summary())

    # save best model
    model.save(MODEL_PATH / "keras_model")

main()