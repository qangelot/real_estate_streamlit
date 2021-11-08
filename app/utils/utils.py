import pandas as pd
import time
import logging
from functools import wraps
import streamlit as st
from typing import List
from tqdm import tqdm


YEARS = ['2021', '2020', '2019', '2018', '2017', '2016']

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


@st.cache(persist=True, allow_output_mutation=True)
def datasets_merging():

    merged_df = dfs[YEARS[0]]
    merged_df.set_index('date_mutation', inplace=True)
    for year in dfs.keys():
        if year != YEARS[0]:
            dfs[year].set_index('date_mutation', inplace=True)
            merged_df = pd.concat([merged_df, dfs[year]])
            
    return merged_df


# preprocess dataset for analysis
@timed
@st.cache(persist=True, allow_output_mutation=True)
def preprocess_data(data):
    
    df = pd.read_csv(f'../data/{data}.csv', sep=',', header=0, low_memory=False)
    df = optimize_floats(optimize_ints(optimize_objects(df, 'date_mutation')))
    
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis="columns", inplace=True)

    # derive features based on datetime column
    df['mois_mutation']=df['date_mutation'].dt.month

    to_handle = ['valeur_fonciere', 'nombre_lots', 'surface_reelle_bati', 'nombre_pieces_principales', 'surface_terrain']
    for col in to_handle:
        df = zscore_outliers(df, col, 2)

    return df


datas = ["clean_sample_2021", "clean_sample_2020", "clean_sample_2019", "clean_sample_2018", "clean_sample_2017", "clean_sample_2016"]
dfs = dict()
for data in tqdm(datas):
    year = data[-4:]
    dfs[str(year)] = preprocess_data(data)

merged_df = datasets_merging()