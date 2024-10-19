import os

import numpy as np
import onnxruntime
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load the ONNX model
model_path = os.getenv("ONNX_MODEL_PATH")
session = onnxruntime.InferenceSession(model_path)
input_names = [inp.name for inp in session.get_inputs()]
output_names = [out.name for out in session.get_outputs()]


# Define a Pydantic model for the input data
class PredictionRequest(BaseModel):
    Material_A_Charged_Amount: float
    Material_B_Charged_Amount: float
    Reactor_Volume: float
    Material_A_Final_Concentration_Previous_Batch: float


# Define a prediction route
@app.post("/predict")
async def predict(request: PredictionRequest):
    # Prepare input data for the model
    input_data = {
        "Material_A_Charged_Amount": np.array(
            [[request.Material_A_Charged_Amount]], dtype=np.float32
        ),
        "Material_B_Charged_Amount": np.array(
            [[request.Material_B_Charged_Amount]], dtype=np.float32
        ),
        "Reactor_Volume": np.array([[request.Reactor_Volume]], dtype=np.float32),
        "Material_A_Final_Concentration_Previous_Batch": np.array(
            [[request.Material_A_Final_Concentration_Previous_Batch]], dtype=np.float32
        ),
    }

    # Run the ONNX model to get predictions
    result = session.run(output_names, input_data)

    # Return the prediction results
    return {
        "output_label": result[0][0],  # Assuming output_label is a single value
        "output_probability": result[1][
            0
        ],  # Assuming output_probability is a single value
    }


# To run the FastAPI server, use: uvicorn main:app --reload
