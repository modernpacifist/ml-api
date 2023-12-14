### Requirements
[Poetry](https://python-poetry.org/docs/) package >= 1.4

### Run
### Via poetry
```
$ cd ./src
$ poetry install
$ poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### Via Docker
```
$ docker-compose up
```

### Usage
http://81.200.147.126:8000/ - temporary VPS where you can try this API out.  
The service uses FastApi as a REST handler so navigate to [/docs](http://81.200.147.126:8000/docs) for further exploration.  

#### Request-Response example:
Request:  
```sh
curl -X 'POST' \
  'http://81.200.147.126:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "SkillFactory_Id": 1,
  "BirthDate": "1988-07-21",
  "education": "Высшее - специалист",
  "employment_status": "Работаю по найму полный рабочий день/служу",
  "Value": "9 - 10 лет",
  "JobStartDate": "2013-09-01",
  "Position": "начальник п",
  "MonthProfit": 180000,
  "MonthExpense": 90000,
  "Gender": 0,
  "Family_status": "Никогда в браке не состоял(а)",
  "ChildCount": 0,
  "SNILS": 0,
  "Merch_code": 77,
  "Loan_amount": 137000,
  "Loan_term": 18,
  "Goods_category": "Furniture"
}
```
Response:
```sh
{
  "Prediction": [
    {
      "BankA_decision": 0.9749183655,
      "BankB_decision": 0.849627912,
      "BankC_decision": 0.9924119711,
      "BankD_decision": 0.9652436972,
      "BankE_decision": 0.2378726006
    }
  ]
}
```
