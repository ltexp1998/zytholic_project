import pandas as pd
import numpy as np

from sklearn import set_config

set_config(display='diagram')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler, RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_transformer


class BaseModelRev():
    """"
    To be used with the following sequence:
        - get_data()
        - set_preprocess_pipeline()
        - process_data()
        - fit()
    """
    def __init__(self):
        pass

    def get_data(self):
        """Merge data from Beers and Breweries using top-information as referenc"""
        dfbrew = pd.read_csv(
            "../raw_data/Beers_Breweries_and_Beer Reviews/breweries.csv")
        dfbeer = pd.read_csv("../raw_data/beers_style_renamed.csv")
        dftop = pd.read_csv("../raw_data/top_beer_info_style_renamed.csv")

        #read correspondance brewery
        corres_xls = pd.read_excel(
            '../assets/correspondance_breweryclean2.xlsx')
        corres_xls.drop(columns='Unnamed: 0', inplace=True)
        corres_xls.set_index(1, inplace=True)
        corres = corres_xls.to_dict()

        # Renames columns from brewery df to perform merge
        dfbrew = dfbrew.rename(columns={"name": "brewery", "id": "brewery_id"})
        dfbrew['brewery'].replace(corres[0], inplace=True)

        # Merge Beers and Breweries with Top-Information
        dfbrewb = pd.merge(dfbeer,
                           dfbrew[['brewery_id', 'brewery']],
                           how='left',
                           on=['brewery_id'])
        dftopbrew = pd.merge(
            dftop,
            dfbrewb[['id','name', 'brewery', 'state', 'country', 'retired']],
            how='inner',
            on=['name', 'brewery'])

        # Clean dataframe after merge, removes unwanted columns
        # removes retired beers
        working_df = dftopbrew.drop(['description', 'key', 'style key'],
                                    axis=1).drop_duplicates()
        working_df = working_df[working_df.retired == 'f']
        working_df.shape
        working_df['style'] = [
            st.split(' - ')[0] for st in working_df['style']
        ]
        self.working_df = working_df
        return self

    """def get_data_rev(self):"""
        #"""Merge data from Reviews and All the rest using id as referenc"""
        #"""dfrev = pd.read_csv(
            #"../raw_data/Beers_Breweries_and_Beer Reviews/reviews.csv")

        #working_df = self.working_df.rename(columns={"id": "beer_id"})

        #revdf = pd.merge(working_df,
                         #dfrev[['brewery_id', 'brewery']],
                         #how='left',
                         #on=["beer_id"])"""
