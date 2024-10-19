import os

import onnxruntime

# Load the ONNX model
model_path = os.getenv("ONNX_MODEL_PATH")
session = onnxruntime.InferenceSession(model_path)

for input_var in session.get_inputs():
    # Get input and output information
    input_name = input_var.name
    input_shape = input_var.shape
    input_type = input_var.type
    print(f"Input Name: {input_name}, Shape: {input_shape}, Type: {input_type}")

for output_var in session.get_outputs():
    output_name = output_var.name
    print(f"Output Name: {output_name}")
