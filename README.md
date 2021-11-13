# Streamlit app about DVF datasets

That repository contains the Streamlit dataviz app itself aswell as the scripts and notebooks necessary to explore and preprocess the DVF datasets coming from https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/ website. There is 5 of them : 2016/2017/2018/2019/2020.

## Prerequisites

- Python 3.7 and more. 
- All libraries contained in requirements.txt file.

## Setup

Clone the repo and install the dependancies :

```bash
pip install requirements.txt
```

## Running the app

```
cd /app
streamlit run app.py
```

First run may take some time, for next runs, most of the data will be cached.

## Architecture

Notebooks contain exploratory data analysis steps as well and exploration of some other government datasets that might be of interest to improve analysis (crimes and taxes datas).

Data folder holds the data that have been preprocessed and sampled through notebooks and python script. 

App folder contains the streamlit app itself. It worth mentionning the multiapp.py file that allows for multipages streamlit app implementations. Also, utils.py is called to handle the remaining processing when the app is launching.


## Licence

MIT
