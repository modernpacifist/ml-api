from fastapi import FastAPI, status, Response
from pydantic import ValidationError
from models import InputModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Status": "Healthy"}


@app.post("/predict", status_code=200)
async def predict(input_model: InputModel, response: Response):

    try:
        input_model.Loan_amount
    except ValidationError as e:
        errors = e.errors()
        print(errors)

    # if "" in input_model.values():
        # response.status_code = status.HTTP_400_BAD_REQUEST

    return {"Prediction": "0"}
