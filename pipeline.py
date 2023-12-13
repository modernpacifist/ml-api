import joblib
import json
import pandas as pd
from preprocessing import preprocess_data


# Загрузка предварительно обученной модели
# model = joblib.load('your_model.pkl')
MODELS = joblib.load("./data/models.pkl")

# Загрузка кода предобработки данных
from preprocessing import preprocess_data

# Считайте JSON из файла "input.json"
# with open("./input.json", "r") as file:
    # json_data = file.read()


# pd.set_option('display.max_columns', 999)


# Предсказание по каждому банку отдельно на одобрение рассрочки
def predict(features_json):
    # Разбор JSON-строки
    features = json.loads(features_json)

    # Преобразуйте входные данные JSON в DataFrame
    features_df = pd.DataFrame([features], index=[0])

    # Предскажите вероятности для каждого банка
    predictions = pd.DataFrame()

    # print(MODELS)

    for idx, model in enumerate(MODELS):
        predictions[f"prediction_target{idx+1}"] = model.predict_proba(features_df)[
            :, 0
        ]

    # Преобразуйте DataFrame с предсказаниями в JSON и верните
    return predictions.to_json(orient="records")


def predict_adapter(json_data):
    input_data = preprocess_data(json_data)

    res = predict(input_data)

    return res
