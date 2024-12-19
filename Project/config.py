IS_NOTEBOOK = False
PATH = None
FOLDER = None

if IS_NOTEBOOK:
    PATH = "D:\BigFiles\Projects Programming\Яндекс Специализация осень 2024 (Big Data)\dataset_telemetry.csv"
    FOLDER = "D:\BigFiles\Projects Programming\Яндекс Специализация осень 2024 (Big Data)"
else:
    PATH = "D:\Курсы(образование)\Яндекс Специализации\BigData\Project\dataset_telemetry.csv"
    FOLDER = "D:\Курсы(образование)\Яндекс Специализации\BigData\Project"



import pandas as pd
from IPython.display import display


def get_df(info=True):
    df = pd.read_csv(PATH, index_col=0)
    df['userid'] = df['userid'].map(lambda uid: int(uid.split('_')[-1]))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # df['category'] = df['category'].fillna(value='Not defined')
    if info:
        print(df.info())
        display(df.head(100))
    return df


def save_df(df: pd.DataFrame, fname: str):
    df.to_csv(f'{FOLDER}/{fname}', index=False, header=True)


# ['Авто/мото товары',
# 'Красота и здоровье',
# 'Одежда и обувь',
# 'Продовольственные товары',
# 'Товары для детей',
# 'Электроника и бытовая техника']
