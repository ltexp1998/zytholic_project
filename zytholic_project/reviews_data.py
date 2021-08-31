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
        """Merge data from Beers Breweries and Reviews using top-information as reference"""
        dfbrew = pd.read_csv(
            "../raw_data/Beers_Breweries_and_Beer Reviews/breweries.csv")
        dfbeer = pd.read_csv("../raw_data/beers_style_renamed.csv")
        dftop = pd.read_csv("../raw_data/top_beer_info_style_renamed.csv")
        #dfrev = pd.read_csv("../raw_data/reviews_top_beer_concatenated.csv")

        #read correspondance brewery
        corres_xls = pd.read_csv('../assets/matching_brewery_names.csv')
        corres_xls.set_index('bbr', inplace=True)
        corres = corres_xls.to_dict()

        # Renames columns from brewery df to perform merge
        dfbrew = dfbrew.rename(columns={"name": "brewery", "id": "brewery_id"})
        dfbrew['brewery'].replace(corres['top'], inplace=True)

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
        working_df = working_df.rename(columns={"id": "beer_id"})
        # Merge Beers and Reviews with Top-Information

        # working_df = pd.merge(working_df, dfrev, how='left', on=['beer_id'])
        # working_df = working_df.drop(columns='beer_id')

        #reformat styles
        self.working_df = self.reformat_styles(working_df, ohe=True)
        return self

    def reformat_styles(self, working_df, ohe=True):
        """
        Simplify the columns 'style' of an input DF
        Converts various features insides style name to OHE features
        """

        # Get matching table for styles names and format it
        style_csv = pd.read_csv('../assets/style_convert.csv')
        style_csv = style_csv[['Converted', 'Simplified']]

        # creation of a dictionary to replace automatically
        style_dict = style_csv.set_index('Converted').to_dict()
        style_dict = style_dict['Simplified']
        style_dict

        #styles_test = working_df[['style']].drop_duplicates()
        working_df['simple_style'] = working_df['style'].replace(style_dict)

        # One-Hot-Encoding of featrues_to_implement
        features_to_implement = [
            'milk', 'old', 'dark', 'wild', 'pale', 'red', 'imperial'
        ]
        if ohe:
            for feat in features_to_implement:
                working_df[feat] = [
                    1 if feat in elm.lower() else 0
                    for elm in working_df['style']
                ]

        working_df.rename(columns={
            'style': 'original_style',
            'simple_style': 'style'
        },
                          inplace=True)
        return working_df
