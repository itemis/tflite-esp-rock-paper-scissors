#!/bin/bash
echo "Converting tflite model to c array"
MODEL_PATH=bin_model
xxd -i $MODEL_PATH/lite_model.tflite > $MODEL_PATH/model_hexgraph.cc