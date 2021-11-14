import numpy as np
import pandas as pd
from typing import List
from tqdm import tqdm 


# Memory usage optimization functions

def optimize_floats(df: pd.DataFrame) -> pd.DataFrame:
    ''' apply the lowest float dtype possible '''
    floats = df.select_dtypes(include=['float64']).columns.tolist()
    df[floats] = df[floats].apply(pd.to_numeric, downcast='float')
    return df


def optimize_ints(df: pd.DataFrame) -> pd.DataFrame:
    ''' apply the lowest int dtype possible '''
    ints = df.select_dtypes(include=['int64']).columns.tolist()
    df[ints] = df[ints].apply(pd.to_numeric, downcast='integer')
    return df


def optimize_objects(df: pd.DataFrame, datetime_features: List[str]) -> pd.DataFrame:
    ''' apply the category dtype to object '''
    for col in df.select_dtypes(include=['object']):
        if col not in datetime_features:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if float(num_unique_values) / num_total_values < 0.5:
                df[col] = df[col].astype('category')
        else:
            df[col] = pd.to_datetime(df[col])
    return df
    

# cleaning and sampling DVF datasets

def preprocessing(data, frac=.3):

    data = pd.read_csv(f'app/{data}', sep=',', header=0, low_memory=False)
    data = optimize_floats(optimize_ints(optimize_objects(data, 'date_mutation')))

    # remove useless columns 
    data = data[data.columns[data.isna().sum()/data.shape[0] <= 0.9]]
    data.drop(['id_mutation', 'id_parcelle', 'code_postal', 'code_type_local', 'code_commune', 'adresse_numero', 'adresse_code_voie', 'adresse_nom_voie', 'code_nature_culture'], inplace=True, axis=1)

    # sampling the datasets because of CPU/RAM limits
    sampled = data.sample(frac = frac)

    return sampled


datas = ["data/data_2021.csv", "data/data_2020.csv", "data/data_2019.csv", "data/data_2018.csv", "data/data_2017.csv", "data/data_2016.csv"]
for data in tqdm(datas):
    year = data[-8:-4]
    if year == "2016" or year == "2021":
        # higher sampling for 2016 and 2021 because less data points
        data_cleaned = preprocessing(data, frac=.6)
    else:
        data_cleaned = preprocessing(data)
    data_cleaned.to_csv(f'app/data/clean_sample_{year}.csv', index=False)

