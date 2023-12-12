from pydantic import BaseModel


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
