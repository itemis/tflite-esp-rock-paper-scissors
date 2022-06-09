"""
References
General conversion https://www.tensorflow.org/lite/convert?hl=en
Post-training quantization https://www.tensorflow.org/lite/performance/post_training_quantization?hl=en
"""
import sys
from pathlib import Path

import tensorflow as tf
import numpy as np
# use netron from command line instead
# import netron

sys.path.append(str(Path(__file__).parents[2].resolve()))
from src.keras_model.dataset import train_ds

KERAS_MODEL_PATH = Path("bin_model") / "keras_model"
assert KERAS_MODEL_PATH.exists(), "The path to your Keras model does not exist!"
LITE_MODEL_PATH = Path("bin_model") / "lite_model.tflite"
FULL_QUANTIZATION = False
NUM_EXAMPLES_IN_REP_DATASET = 300   # number of examples in the representative dataset
                                    # 100-300 is a good value according to TF doc


# model conversion is based upon behavior on real data using forward passes
def representative_dataset():
    """
    len(train_ds.as_numpy_iterator) == 100
    len(batch) == 2
    batch[0].shape == (32, 240, 240, 3)
    batch[1].shape == (32, 3)
    """
    img_count = 0
    for batch in train_ds.as_numpy_iterator():
        for img in batch[0]:
            data = tf.expand_dims(img, axis=0) # re-wrap into a batch of 1 img
            data = data.numpy()
            data = data.astype(np.float32)
            img_count += 1
            yield [data]
            
            if img_count == NUM_EXAMPLES_IN_REP_DATASET: break
        
        if img_count == NUM_EXAMPLES_IN_REP_DATASET: break

# initialize converter
converter = tf.lite.TFLiteConverter.from_saved_model(str(KERAS_MODEL_PATH))

# define microcontroller optimization such as 8-bit quantization
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
if FULL_QUANTIZATION:
    # whether to fully quantize
    # in the TinyML book this is missing
    # the TF documentation recommends this

    # NOTE: uint8 is deprecated in tflite-micro 
    # https://github.com/tensorflow/tflite-micro/issues/216
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8
tflite_quant_model = converter.convert()

# apply conversion
tflite_model = converter.convert()

# save tf_lite model
with open(LITE_MODEL_PATH, 'wb') as f:
    f.write(tflite_model)

# visualize tflite model
# saving is an open issue 
# https://github.com/lutzroeder/netron/issues/162
# netron.start(LITE_MODEL_PATH)