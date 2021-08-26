import pandas as pd
import numpy as np

from sklearn import set_config; set_config(display='diagram')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
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
        """Merge data from Beers and Breweries using top-information as reference"""
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
        self.working_df = self.reformat_styles(working_df, ohe=True)
        return self
    
    def reformat_styles(self, working_df, ohe=True):
        """
        Simplify the columns 'style' of an input DF
        Converts various features insides style name to OHE features
        """
        
        # Get matching table for styles names and format it
        style_xls = pd.read_excel('../assets/style_convert.xlsx')
        style_xls.columns = style_xls.iloc[0, :]
        style_xls = style_xls.iloc[1:, 1:]

        # creation of a dictionary to replace automatically
        style_dict = style_xls.set_index('Converted').to_dict()
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

    def process_data(self):
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

    def fit(self, clusts=20):
        """Actual fit using KMeans algorithm"""
        self.kmeans_fit = KMeans(n_clusters=clusts)
        self.kmeans_fit.fit(self.X_train_proc)
        return self
    
   
def content(df, name, sim_matrix=None, n_recomm=10):
    """
    Uses similarity distance using sim_matrix to return the 10 closest beers
    to the "name" input inside the specified DF
    """
    
    # Dataframe to get index of a given beer
    temp = df.copy()
    temp.reset_index(drop=True, inplace=True)
    temp.reset_index(inplace=True)
    index = temp.iloc[:,:4]
    
    # Extract most similar beers
    position = index[index.name == name]['index']
    score = sorted(
        list(enumerate(sim_matrix[position][0])),
        key=lambda x:x[1],reverse=True)
    indices = score[1:n_recomm+1]
    beers_indices = [i[0] for i in indices]
    # Top 10 most similar beers
    return df.iloc[beers_indices]

def evaluate_proximity(df,  n_recomm=10, tests=10, sim_matrix=None,):
    """
    For each style in a give dataframe, return percentage of recommendations
    that have the same style and the number of items of said style in the DF
    """
    df_styles = df['style'].value_counts()

    results = []
    mod_list = []
    # Explore each style
    for st in df_styles.index:
    # Get a few random samples
        samples = df[df['style'] == st]['name']
        samples = samples.sample(min(tests, len(samples)))

        percent = []
        mod = {}
        for name in samples:
            # calculate content based similarity for each sample
            res = content(df, name, sim_matrix, n_recomm)
            # Get percentage of matching style for each sample
            matching_percent = res[res['style'] == st].shape[0] / res.shape[0] * 100
            percent.append(matching_percent)
            
            # count which are the most suggested labels
            dict_count = res.value_counts('style').to_dict()
            for lab, val in dict_count.items():
                value = mod.get(lab, 0)
                mod[lab] = value + val
        
        # average for each style    
        style_result = np.array(percent).mean()
        results.append(style_result)
        
        val_counts = pd.Series(mod).sort_values(ascending=False).reset_index()
        mod_list.append(val_counts.iloc[0, 0])
    
    final_style = df_styles.reset_index()
    final_style['matching_percent'] = results
    final_style['mod'] = mod_list
    return final_style