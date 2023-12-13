import json
from fastapi import FastAPI, Response
from pydantic import ValidationError

from pydantic import BaseModel
from pipeline import predict_adapter


app = FastAPI()


class InputModel(BaseModel):
    BirthDate: str
    education: str
    employment_status: str
    Value: str
    JobStartDate: str
    Position: str
    MonthProfit: int
    MonthExpense: int
    Gender: int
    Family_status: str
    ChildCount: int
    SNILS: int
    Merch_code: int
    Loan_amount: int
    Loan_term: int
    Goods_category: str


@app.get("/")
async def read_root():
    return {"Status": "Healthy"}


@app.post("/predict", status_code=200)
async def predict(input_model: InputModel, response: Response):

    try:
        prediction_result = predict_adapter(input_model.model_dump_json())

    except ValidationError as e:
        errors = e.errors()
        print(errors)
        prediction_result = ""
        # TODO: return 400 <13-12-23, modernpacifist> #

    return {"Prediction": prediction_result}
