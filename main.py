from fastapi import FastAPI, status, Response
from models import InputModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Status": "Healthy"}


@app.post("/predict", status_code=201)
async def predict(input_model: InputModel, response: Response):

    input_model.Loan_amount

    # if "" in input_model.values():
        # response.status_code = status.HTTP_400_BAD_REQUEST

    return {"Prediction": "0"}
