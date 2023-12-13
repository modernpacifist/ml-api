import joblib
import json
import pandas as pd
from preprocessing import preprocess_data


# Загрузка предварительно обученной модели
MODELS = joblib.load("./data/models.pkl")


# Предсказание по каждому банку отдельно на одобрение рассрочки
def predict(features_json):
    # Разбор JSON-строки
    features = json.loads(features_json)

    # Преобразуйте входные данные JSON в DataFrame
    features_df = pd.DataFrame([features], index=[0])

    # Предскажите вероятности для каждого банка
    predictions = pd.DataFrame()

    bank_list = [
        "BankA_decision",
        "BankB_decision",
        "BankC_decision",
        "BankD_decision",
        "BankE_decision",
    ]

    for idx, model in enumerate(MODELS):
        try:
            predictions[bank_list[idx]] = model.predict_proba(features_df)[
                :, 0
            ]
        except IndexError:
            break

    # Преобразуйте DataFrame с предсказаниями в JSON и верните
    return predictions.to_json(orient="records")


def predict_adapter(json_data):
    input_data = preprocess_data(json_data)
    
    return json.loads(predict(input_data))
