import numpy as np
import pandas as pd
from nltk.stem import SnowballStemmer
from pymystem3 import Mystem
import nltk
import re
from nltk.corpus import stopwords
from datetime import date
from sklearn.preprocessing import LabelEncoder
from joblib import load
import json

# Фиксируем сиид
np.random.seed(42)


# Фун-ция обработки данныхк типа времени
def convert_object_to_datetime(df, columns, str_format):
    for column in columns:
        if not column in df.columns:
            continue
        df[column] = pd.to_datetime(df[column], format=str_format)

    print("Conversion of the date column is completed ")
    return df


# Функция для простой предварительной обработки строковых данных
def preproc_string_col(dataframe, column):
    df_func = dataframe.copy()
    df_func.loc[:, column] = df_func[column].astype(str)
    df_func.loc[:, column] = df_func[column].str.strip()
    df_func.loc[:, column] = df_func[column].str.lower()
    df_func.loc[:, column] = df_func[column].apply(lambda x: re.sub(r"[^\w\s]", "", x))

    print(f"Preprocessing of string column {column} finished")
    return df_func


# Функция для обработки стобцов с датами
def datetime_preproc(df):
    df_func = df.copy()

    # Приводим столбцы с датами к типу datetime
    df_func = convert_object_to_datetime(df_func, ["BirthDate", "JobStartDate"], "%Y-%m-%d")
    # df_func = convert_object_to_datetime(df_func, [], "%Y-%m-%d")

    # Вычисляем столбцы в днях
    today = pd.to_datetime(date.today())

    df_func["Age"] = (today - df_func["BirthDate"]).dt.days

    df_func["Experience"] = (today - df_func["JobStartDate"]).dt.days

    # Удаляем ненужные столбцы
    df_func = df_func.drop(["BirthDate", "JobStartDate"], axis=1)

    print("Preprocessing of datetime column end")
    return df_func


# Функция для приведения категориальных столбцов
def label_encoder_preproc(df, name_column, new_name_column, file_name):
    df_func = df.copy()

    # Загружаем сохраненный кодировщик меток, полученный при обработке исходного датафрейма
    loaded_label_encoder = load(file_name)

    # Преобразование новых категорий в числовые коды
    df_func[new_name_column] = loaded_label_encoder.transform(
        df_func[name_column].astype(str)
    )

    # Присваиваем новым категориям, которые мы не встречали, новое значение
    df_func.loc[
        ~df_func[name_column].isin(loaded_label_encoder.classes_), new_name_column
    ] = 999

    df_func = df_func.drop([name_column], axis=1)

    print("Preprocessing of lavle column end")
    return df_func


# Решение проблем error от банка
def process_bank_error(column):
    # success = 0, denied = 1, error = 2
    # наша задача заменить error 2 на средний ответ других банков
    # алгоритм: Если другой банк одобрил заявку, рейтинг человек +1
    # если отказал, рейтинг -1
    # итог, если рейтинг больше 0, то мы заменяем error 2 на success 0
    # иначе на denied 1
    rating = 0
    for i in range(len(column)):
        if column[i] == 2:
            for j in range(len(column)):
                if j != i:
                    if column[j] == 0:
                        rating += 1
                    elif column[j] == 1:
                        rating -= 1
            if rating > 0:
                column[i] = 0
            else:
                column[i] = 1
            rating = 0
    return column


# # Считайте JSON из фходного файла "input.json"
# with open("input.json", "r") as file:
    # input_json = file.read()
# features = json.loads(input_json)
# # Преобразуйте входные данные JSON в DataFrame
# df = pd.DataFrame([features], index=[0])


# наша функция для вызова в pipeline
def preprocess_data(json_data):
    # Создание DataFrame из json
    data_dict = json.loads(json_data)
    df = pd.DataFrame([data_dict])

    # Дропаем ненужный столбец сразу
    if "SkillFactory_Id" in df.columns:
        print("SkillFactory_Id was dropped")
        df = df.drop(["SkillFactory_Id"], axis=1)

    # Преобработка столбцов BirthDate и JobStartDate
    df = datetime_preproc(df)

    # Преобработка столбца education
    df = preproc_string_col(df, "education")
    df = label_encoder_preproc(
        df=df,
        name_column="education",
        new_name_column="Education_encoded",
        file_name="./data/education_encoder.joblib",
    )

    # Преобработка столбца employment status
    df = preproc_string_col(df, "employment_status")
    df = label_encoder_preproc(
        df=df,
        name_column="employment_status",
        new_name_column="Empl_status_encoded",
        file_name="./data/empl_status_encoder.joblib",
    )

    # Преобработка столбца Value
    df = preproc_string_col(df, "Value")
    df = label_encoder_preproc(
        df=df,
        name_column="Value",
        new_name_column="Value_encoded",
        file_name="./data/value_encoder.joblib",
    )

    # Преобработка столбца Family status
    df = preproc_string_col(df, "Family_status")
    df = label_encoder_preproc(
        df=df,
        name_column="Family_status",
        new_name_column="Family_status_encoded",
        file_name="./data/family_status_encoder.joblib",
    )

    # Преобработка столбца Goods_category
    df = preproc_string_col(df, "Goods_category")
    df = label_encoder_preproc(
        df=df,
        name_column="Goods_category",
        new_name_column="Goods_category_encoded",
        file_name="./data/goods_category_encoder.joblib",
    )

    # Базовая и дополнительная базовая предобработка строк
    df = preproc_string_col(df, "Position")
    nltk.download("stopwords")
    stop_words = set(stopwords.words("russian"))
    df["Position"] = df["Position"].apply(
        lambda x: " ".join(
            [word for word in x.split() if word.lower() not in stop_words]
        )
    )

    # Лемминг и стреминг
    # Инициализация стеммера SnowballStemmer
    stemmer = SnowballStemmer("russian")
    # Стемминг с использованием SnowballStemmer
    df["Stemms"] = df["Position"].apply(
        lambda x: " ".join([stemmer.stem(word) for word in x.split()]).strip()
    )

    # Инициализация лемматизатора Mystem
    mystem = Mystem()
    # Лемматизация с использованием Mystem
    df["Pos_end"] = df["Stemms"].apply(lambda x: " ".join(mystem.lemmatize(x)).strip())

    # Ручная обработка должностей к единому виду
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "менеджер" if "менед" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "помощник" if "пом" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "программист" if "прог" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "бухгалтер" if "бухг" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(
        lambda x: "директор или зам" if "дирек" in x else x
    )
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "заведующий" if "завед" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(
        lambda x: "руководитель" if "руковод" in x else x
    )
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "учитель" if "учи" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "самозанятый" if "самоз" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "оператор" if "операт" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "мастер" if "мастер" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "бригадир" if "бриг" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "механик" if "мех" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "начальник" if "нача" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "продавец" if "прода" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "администратор" if "адм" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "уборщик" if "убор" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "монтажник" if "монта" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "инспектор" if "инсп" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "монтер" if "монте" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "инженер" if "инж" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "охранник" if "охр" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "мед персонал" if "мед" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "врач" if "вра" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "курьер" if "кур" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "рабочий" if "рабоч" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(
        lambda x: "производитель" if "произв" in x else x
    )
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "водитель" if "водитель" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "психолог" if "псих" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "токарь" if "ток" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "кассир" if "кас" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "сотрудник" if "сотр" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "слесарь" if "слес" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "организатор" if "орган" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "фрилансер" if "фри" in x else x)
    df["Pos_end"] = df["Pos_end"].apply(lambda x: "юрист" if "юр" in x else x)

    # Преобработка столбца Goods_category
    df = preproc_string_col(df, "Pos_end")
    df = label_encoder_preproc(
        df=df,
        name_column="Pos_end",
        new_name_column="Pos_сategory",
        file_name="./data/pos_сategory_encoder.joblib",
    )

    df = df.drop(["Stemms", "Position"], axis=1)

    # Правка денежных значений зп/расход
    # фильтр: если зарплата меньше 1000, умножить на 1000
    df["MonthProfit"] = np.where(
        df["MonthProfit"] > 999, df["MonthProfit"], df["MonthProfit"] * 1000
    )
    df["MonthExpense"] = np.where(
        df["MonthExpense"] > 999, df["MonthExpense"], df["MonthExpense"] * 1000
    )

    df['Balance_per_month'] = df['MonthProfit'] - df['MonthExpense']

    df = df.reset_index(drop=True)

    # Делаем реиндекс для однообразности
    desired_column_order = [
        "MonthProfit",
        "MonthExpense",
        "Gender",
        "ChildCount",
        "SNILS",
        "Merch_code",
        "Loan_amount",
        "Loan_term",
        "Education_encoded",
        "Empl_status_encoded",
        "Value_encoded",
        "Family_status_encoded",
        "Goods_category_encoded",
        "Age",
        "Experience",
        "Balance_per_month",
        # "BankA_decision",
        # "BankB_decision",
        # "BankC_decision",
        # "BankD_decision",
        # "BankE_decision",
    ]

    # Используем .reindex(), чтобы изменить порядок столбцов
    df = df.reindex(columns=desired_column_order)

    json_data = df.to_json(orient="records", lines=True)
    return json_data
