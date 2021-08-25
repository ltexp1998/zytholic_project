import pandas as pd
import numpy as np

from sklearn import set_config; set_config(display='diagram')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler, RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_transformer

class BaseModel():
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
        dfbrew = pd.read_csv("../raw_data/Beers_Breweries_and_Beer Reviews/breweries.csv")
        dfbeer = pd.read_csv("../raw_data/beers_style_renamed.csv")
        dftop = pd.read_csv("../raw_data/top_beer_info_style_renamed.csv")

        #read correspondance brewery
        corres_xls = pd.read_excel('../assets/correspondance_breweryclean2.xlsx')
        corres_xls.drop(columns='Unnamed: 0', inplace=True)
        corres_xls.set_index(1, inplace=True)
        corres= corres_xls.to_dict()

        # Renames columns from brewery df to perform merge
        dfbrew = dfbrew.rename(columns={"name": "brewery",
                                        "id": "brewery_id"})
        dfbrew['brewery'].replace(corres[0], inplace=True)

        # Merge Beers and Breweries with Top-Information
        dfbrewb =  pd.merge(dfbeer,
                            dfbrew[['brewery_id','brewery']],
                            how='left',on=['brewery_id'])
        dftopbrew = pd.merge(dftop,
                            dfbrewb[['name', 'brewery', 'state', 'country', 'retired']],
                            how='inner',on=['name','brewery'])

        # Clean dataframe after merge, removes unwanted columns 
        # removes retired beers
        working_df = dftopbrew.drop(['description', 'key', 'style key'], axis= 1).drop_duplicates()
        working_df = working_df[working_df.retired == 'f']
        working_df.shape
        working_df['style'] = [st.split(' - ')[0] for st in working_df['style']]
        self.working_df = working_df
        return self


    # ----------------- PIPELINES ------------------------------
    def set_preprocess_pipeline(self):
        """Create preprocessing pipeline for the data frame"""
        pipe_style_country = make_pipeline(OneHotEncoder(sparse=False, 
                                                        handle_unknown='ignore'))
        pipe_abv_rating = make_pipeline(StandardScaler())
        pipe_taste_features = make_pipeline(MinMaxScaler())
        pipe_state = make_pipeline(
            SimpleImputer(strategy='constant', fill_value=''),
            OneHotEncoder(sparse=False, handle_unknown='ignore')
        )

        # list of numeric columns for min-max scaler
        tastes_features = self.working_df.select_dtypes(np.number).columns[2:]

        # Combine the preprocessing pipelines
        preprocess = make_column_transformer(
            (pipe_style_country, ['style', 'country']),
            (pipe_state, ['state']),
            (pipe_abv_rating, ['abv', 'ave rating']),
            (pipe_taste_features, tastes_features) 
        )
        self.preprocess = preprocess
        return self

    def process_data(self):
        """Split dataset before fitting the model"""
        X_train, X_test = train_test_split(self.working_df, test_size=0.25)
        self.X_train = X_train
        self.X_test = X_test
        self.preprocess.fit(X_train)
        self.X = self.preprocess.transform(X_train)
        self.y = self.preprocess.transform(X_test)
        return self

    def fit(self, clusts=20):
        """Actual fit using KMeans algorithm"""
        self.kmeans_fit = KMeans(n_clusters=clusts)
        self.kmeans_fit.fit(self.X)
        return self