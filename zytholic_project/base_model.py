import pandas as pd
import numpy as np

from sklearn import set_config; set_config(display='diagram')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline

from sklearn.compose import make_column_transformer
from sklearn.metrics.pairwise import cosine_similarity, sigmoid_kernel,linear_kernel
import joblib
import pickle

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
        """Merge data from Beers and Breweries using top-information as reference"""
        dfbrew = pd.read_csv("raw_data/Beers_Breweries_and_Beer Reviews/breweries.csv")
        dfbeer = pd.read_csv("raw_data/beers_style_renamed.csv")
        dftop = pd.read_csv("raw_data/top_beer_info_style_renamed.csv")

        #read correspondance brewery
        corres_xls = pd.read_csv('assets/matching_brewery_names.csv')
        corres_xls.set_index('bbr', inplace=True)
        corres= corres_xls.to_dict()

        # Renames columns from brewery df to perform merge
        dfbrew = dfbrew.rename(columns={"name": "brewery",
                                        "id": "brewery_id"})
        dfbrew['brewery'].replace(corres['top'], inplace=True)

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
        working_df.reset_index(inplace=True, drop=True)
        self.working_df = self.reformat_styles(working_df, ohe=True)
        return self

    def reformat_styles(self, working_df, ohe=True):
        """
        Simplify the columns 'style' of an input DF
        Converts various features insides style name to OHE features
        """

        # Get matching table for styles names and format it
        style_csv = pd.read_csv('assets/style_convert.csv')
        style_csv = style_csv[['Converted', 'Simplified']]

        # creation of a dictionary to replace automatically
        style_dict = style_csv.set_index('Converted').to_dict()
        style_dict = style_dict['Simplified']
        style_dict

        #styles_test = working_df[['style']].drop_duplicates()
        working_df['simple_style'] = working_df['style'].replace(style_dict)

        # One-Hot-Encoding of featrues_to_implement
        features_to_implement = ['milk', 'old', 'dark', 'wild', 'pale', 'red', 'imperial']
        if ohe:
            for feat in features_to_implement:
                working_df[feat] = [1 if feat in elm.lower() else 0 for elm in working_df['style']]

        working_df.rename(columns={'style':'original_style', 'simple_style':'style'}, inplace=True)
        return working_df


    # ----------------- PIPELINES ------------------------------
    def set_preprocess_pipeline(self):
        """Create preprocessing pipeline for the data frame"""
        pipe_style_country = make_pipeline(OneHotEncoder(sparse=False,
                                                        handle_unknown='ignore'))
        num_features_top = make_pipeline(MinMaxScaler())
        # pipe_state = make_pipeline(
        #     SimpleImputer(strategy='constant', fill_value=''),
        #     OneHotEncoder(sparse=False, handle_unknown='ignore')
        # )

        # list of numeric columns for min-max scaler
        tastes_features = self.working_df.select_dtypes(np.number).columns

        # Combine the preprocessing pipelines
        preprocess = make_column_transformer(
            ## Uncomment pipe_state and activate
            #(pipe_state, ['state']),
            (pipe_style_country, ['style',
                                  ##'country' # Deactivated beacause decreases recommendation
                                  ## accuracy, as to many OHE variables relate to geography
                                  ]),
            (num_features_top, tastes_features)
        )
        self.preprocess = preprocess
        return self

    def train_test_process_data(self):
        """Split dataset before fitting the model"""
        X_train, X_test = train_test_split(self.working_df,
                                           test_size=0.25,
                                           stratify=self.working_df['style'])
        self.X_train = X_train
        self.X_test = X_test
        self.preprocess.fit(X_train)
        self.X_train_proc = self.preprocess.transform(X_train)
        self.X_test_proc = self.preprocess.transform(X_test)
        return self
    
    def process_whole_dataset(self):
        """Fit the pipeline on the whole dataset
        Returns np array for matrix distance calculation"""
        self.preprocess.fit(self.working_df)
        self.X = self.preprocess.transform(self.working_df)
        return self
    

        
    def calculate_distances(self):
        """
        Calculate 3 similarity matrices for cosine, sigmoid and linear distance
        The data are saved as 'Float32' to reduce size on disk
        """
        self.cosine_sim = cosine_similarity(self.X, self.X).astype("float32")
        self.sigmoid_sim = sigmoid_kernel(self.X,  self.X).astype("float32")
        self.linear_sim = linear_kernel(self.X, self.X).astype("float32")
        print('Datafile with similarity distances saved')
        return self

    def save_model(self):
        """Save model with original and preprocessed data as a joblib"""
        with open("assets/dataframe.pkl", "wb") as file:
            pickle.dump(self.working_df, file)
        with open("assets/cosine.pkl", "wb") as file:
            pickle.dump(self.cosine_sim, file)
        with open("assets/sigmoid.pkl", "wb") as file:
            pickle.dump(self.sigmoid_sim, file)
        print('Model saved')
        pass
    
    
if __name__ == '__main__':
    model = BaseModel()
    model.get_data()
    model.set_preprocess_pipeline()
    model.process_whole_dataset()
    model.calculate_distances()
    model.save_model()
    print('Initialization complete ! The CSVs and for the API are ready')