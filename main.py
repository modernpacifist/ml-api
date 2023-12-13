from fastapi import FastAPI, status, Response
from pydantic import ValidationError

from pydantic import BaseModel

from pipeline import predict_adapter


app = FastAPI()


# "SkillFactory_Id": 1,
# "BirthDate": "1988-07-21",
# "education": "Высшее - специалист",
# "employment_status": "Работаю по найму полный рабочий день/служу",
# "Value": "9 - 10 лет",
# "JobStartDate": "2013-09-01",
# "Position": "начальник п",
# "MonthProfit": 180000,
# "MonthExpense": 90000,
# "Gender": 0,
# "Family_status": "Никогда в браке не состоял(а)",
# "ChildCount": 0,
# "SNILS": 0,
# "Merch_code": 77,
# "Loan_amount": 137000,
# "Loan_term": 18,
# "Goods_category": "Furniture"
class InputModel(BaseModel):
    BirthDate: str
    Education: str
    EmploymentStatus: str
    Value: str
    JobStartDate: str
    Position: str
    MonthProfit: int
    MonthExpense: int
    Gender: int
    FamilyStatus: str
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
        # input_model.Loan_amount
        prediction_result = predict_adapter(input_model)

    except ValidationError as e:
        errors = e.errors()
        print(errors)

    # if "" in input_model.values():
        # response.status_code = status.HTTP_400_BAD_REQUEST

    return {"Prediction": prediction_result}
