import pandas as pd
import time
import logging
from functools import wraps
import streamlit as st
from typing import List


# define the logging
logger = logging.getLogger(__name__)

# Misc logger setup so a debug log statement gets printed on stdout.
logger.setLevel("INFO")
handler = logging.FileHandler('exec_time_logs.txt', mode='a', delay=False)
log_format = "%(asctime)s %(levelname)s -- %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


def timed(func):
    """This decorator prints the execution time for the decorated function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper


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
    

# handle outliers
def zscore_outliers(data, column, n):
    """
    Tag outliers in dataset in regard from a specific column
    In literature, often 3 std from the mean is consider as an outlier
    Return two boolean columns : upper_outlier and lower_outlier
    """

    # here we remove outliers unilateraly, but we could aggregate on meaningful column

    data['lower_bound'] = data[column].mean() - (n * data[column].std())
    data['upper_bound'] = data[column].mean() + (n * data[column].std())

    data["upper_outlier"] = data[column] > data['upper_bound']
    data["lower_outlier"] = data[column] < data['lower_bound']

    data = data.loc[(data['upper_outlier'] != 1) & (data['lower_outlier'] != 1)]

    data.drop(['upper_bound', 'upper_outlier', 'lower_bound', 'lower_outlier'], axis=1, inplace=True)

    return data


# preprocess dataset for analysis
@timed
@st.cache(persist=True)
def preprocess_data():
    
    df = pd.read_csv('../data/sample_enhanced.csv', sep=',', header=0, low_memory=False)
    optimize_floats(optimize_ints(optimize_objects(df, 'date_mutation')))
    
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis="columns", inplace=True)

    # convert to datetime
    df['date_mutation'] =  pd.to_datetime(df['date_mutation'])

    # derive features based on datetime column
    df['mois_mutation']=df['date_mutation'].dt.month

    # remove useless columns 
    df = df[df.columns[df.isna().sum()/df.shape[0] <= 0.9]]
    df.drop(['id_mutation', 'id_parcelle', 'code_postal', 'code_type_local', 'code_commune', 'adresse_numero', 'adresse_code_voie', 'adresse_nom_voie', 'code_nature_culture'], inplace=True, axis=1)

    to_handle = ['valeur_fonciere', 'nombre_lots', 'surface_reelle_bati', 'nombre_pieces_principales', 'surface_terrain']
    for col in to_handle:
        df = zscore_outliers(df, col, 2)

    # création de sous-ensembles has_lot / no_lot
    has_lot = df[df['nombre_lots'] == 1]
    no_lot = df[df['nombre_lots'] == 0]

    return df, has_lot, no_lot

data20, has_lot, no_lot = preprocess_data()