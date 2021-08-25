import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import set_config; set_config(display='diagram')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler, RobustScaler
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_transformer

dfbrew = pd.read_csv("../raw_data/Beers_Breweries_and_Beer Reviews/breweries.csv")
dfbeer = pd.read_csv("../raw_data/beers_style_renamed.csv")
dftop = pd.read_csv("../raw_data/top_beer_info_style_renamed.csv")

#read correspondance brewery
corres_xls = pd.read_excel('../assets/correspondance_breweryclean2.xlsx')
corres_xls.drop(columns='Unnamed: 0', inplace=True)
corres_xls.set_index(1, inplace=True)
corres= corres_xls.to_dict()



dfbrew = dfbrew.rename(columns={"name": "brewery",
                                "id": "brewery_id"})

dfbrew['brewery'].replace(corres[0], inplace=True)

dfbrewb =  pd.merge(dfbeer,dfbrew[['brewery_id','brewery']],how='left',on=['brewery_id'])

dftopbrew = pd.merge(dftop,dfbrewb[['name', 'brewery', 'state', 'country', 'retired']],
                     how='inner',on=['name','brewery'])