from operator import mod
import pandas as pd
from zytholic_project.base_model import BaseModel
from zytholic_project.evaluate import get_recommendations, get_name_index
from sklearn.metrics.pairwise import cosine_similarity, sigmoid_kernel,linear_kernel

def check_name(name):
    """
    Get a name of a beer as an input
    ----
    Returns whether or not the name is in the database
    """
    beer_list = pd.read_csv(
        'raw_data/top_beer_info_style_renamed.csv', 
        usecols=['name'])
    beer_list = beer_list['name'].to_list()
    return name if name in beer_list else 'Invalid Name'


def get_most_similar_beers(name, n_beers=5, similarity='cosine'):
    """
    Check that name is valid
    """
    if check_name(name) != name:
        return {'response': f'{name} is not a valid name'}
    
    # Import data, preprocess it
    # To extract for function and to be executed only once
    model = BaseModel()
    model.get_data()
    model.set_preprocess_pipeline()
    model.preprocess.fit(model.working_df)
    model.X = model.preprocess.transform(model.working_df)
    
    # Get similarity scores between beers
    # To extract for function and to be executed only once
    if similarity == 'cosine':
        kernel = cosine_similarity(model.X, model.X)
    elif similarity == 'sigmoid':
        kernel = sigmoid_kernel(model.X,  model.X)
    elif similarity == 'linear':
        kernel = linear_kernel(model.X, model.X)
    
    results = get_recommendations(model.working_df, name, 
                      sim_matrix=kernel, n_recomm=n_beers)
    results = results[['name', 'brewery', 'style', 'abv', 'min ibu', 'max ibu']]
    
    return results.to_dict()

def get_most_similar_beers_ibu_abv(name,
                           ibu,
                           abv, 
                           n_beers=5, similarity='cosine'):
    """
    Check that name is valid
    """
    if check_name(name) != name:
        return {'response': f'{name} is not a valid name'}
    
    # Import data, preprocess it
    # To extract for function and to be executed only once
    model = BaseModel()
    model.get_data()
    model.set_preprocess_pipeline()
    model.preprocess.fit(model.working_df)
    model.X = model.preprocess.transform(model.working_df)
    
    # Get similarity scores between beers
    # To extract for function and to be executed only once
    if similarity == 'cosine':
        kernel = cosine_similarity(model.X, model.X)
    elif similarity == 'sigmoid':
        kernel = sigmoid_kernel(model.X,  model.X)
    elif similarity == 'linear':
        kernel = linear_kernel(model.X, model.X)
    
    # Filter results if IBU or ABV are specified
    if ibu is not None:
        bad_index_ibu = model.working_df[model.working_df['max ibu'] > ibu] 
        bad_index_ibu = set(bad_index_ibu.index)
    else:
        bad_index_ibu = set()  
                                                 
    if abv is not None:
        bad_index_abv = model.working_df[model.working_df['abv'] > abv]
        bad_index_abv = set(bad_index_abv.index)
    else:
        bad_index_abv = set()  
    
    bad_indexes = bad_index_abv.union(bad_index_ibu)
    # keep current beer position in kernel
    name_position = get_name_index(name, model.working_df)
    bad_indexes.discard(int(name_position))
    bad_indexes = list(bad_indexes)
    
    # Get the recommendation
    results = get_recommendations(
        model.working_df, name, 
        sim_matrix=kernel, 
        n_recomm=n_beers,
        ignore_index_beers=bad_indexes)
    
    results = results[['name', 'brewery', 
                       'style', 'abv', 
                       'min ibu', 'max ibu']]
    
    return results.to_dict()
    
    
if __name__ == '__main__':
    print(check_name('Our Special Ale 2019 (Anchor Christmas Ale)'))
    print(check_name('Gaffel Kölsch'))
    print(check_name('abcde') == 'Invalid Name')
    print(check_name('Longist Trail Ale') == 'Invalid Name')
