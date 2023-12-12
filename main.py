from fastapi import FastAPI, status, Response
from models import InputModel


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Status": "Healthy"}


@app.post("/predict", status_code=201)
async def predict(input: InputModel, response: Response):
    data = input.dict()
    
    if "" in data.values():
        response.status_code = status.HTTP_400_BAD_REQUEST

    return {"Prediction": "0"}
