import pandas as pd
import pickle
from zytholic_project.apicall import get_most_similar_beers
from zytholic_project.filter_out_propositions import filter_bad_countries, filter_bad_abv, filter_bad_ibu


with open("assets/dataframe.pkl", "rb") as file:
    working_df = pickle.load(file)

def test_bad_country_filter():
    # Just a dummy creation for function call
    data = pd.DataFrame.from_dict(
        get_most_similar_beers('Donnybrook Stout', n_beers=8))
    assert filter_bad_countries(data) == []
    
    # Test with a country name
    bad_idx = filter_bad_countries(working_df, 'FR')
    sub_df = working_df.drop(working_df.index[bad_idx])
    assert sub_df['country'].unique()[0] == 'FR'
        
        
def test_filter_bad_abv():
    bad_idx = filter_bad_abv(working_df, 3.1)
    sub_df = working_df.drop(working_df.index[bad_idx])
    assert sub_df['abv'].max() <= 3.1
        
def test_filter_bad_ibu():
    bad_idx = filter_bad_ibu(working_df, 40)
    sub_df = working_df.drop(working_df.index[bad_idx])
    assert sub_df['abv'].max() <= 40