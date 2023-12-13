from fastapi import FastAPI, status, Response
from pydantic import ValidationError

from pydantic import BaseModel


app = FastAPI()


class InputModel(BaseModel):
    BirthDate: str
    Education: str
    EmploymentStatus: str
    Value: int
    JobStartDate: int
    Position: str
    MonthProfit: str
    MonthExpense: str
    Gender: str
    FamilyStatus: str
    ChildCount: str
    SNILS: str
    Merch_code: str
    Loan_amount: str
    Loan_term: str
    Goods_category: str


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
