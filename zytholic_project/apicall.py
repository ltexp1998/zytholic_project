import pandas as pd
from zytholic_project.base_model import BaseModel
from zytholic_project.evaluate import content
from sklearn.metrics.pairwise import cosine_similarity, sigmoid_kernel,linear_kernel

def check_name(name):
    """
    Get a name of a beer as an input
    ----
    Returns whether or not the name is in the database
    """
    beer_list = pd.read_csv('raw_data/top_beer_info_style_renamed.csv', 
                            usecols=['name'])
    beer_list = beer_list['name'].to_list()
    return name if name in beer_list else 'Invalid Name'


def get_most_similar_beers(name, n_beers=5, similarity='cosine'):
    """
    Check that name is valid
    """
    if check_name(name) != name:
        return None
    
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
    
    results = content(model.working_df, name, 
                      sim_matrix=kernel, n_recomm=n_beers)
    results = results[['name', 'brewery', 'style', 'abv']]
    return results
    
    
    
if __name__ == '__main__':
    print(check_name('Our Special Ale 2019 (Anchor Christmas Ale)'))
    print(check_name('Gaffel Kölsch'))
    print(check_name('abcde') == 'Invalid Name')
    print(check_name('Longist Trail Ale') == 'Invalid Name')
