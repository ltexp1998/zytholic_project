from operator import mod
from os import symlink
import pandas as pd
import numpy as np
import pickle
from zytholic_project.base_model import BaseModel
from zytholic_project.evaluate import get_recommendations, get_name_index
from sklearn.metrics.pairwise import cosine_similarity, sigmoid_kernel,linear_kernel
from zytholic_project.filter_out_propositions import bad_country_filter

def check_name(name):
    """
    Get a name of a beer as an input
    ----
    Returns whether or not the name is in the database
    """
    with open('assets/dataframe.pkl', 'rb') as file:
        beer_list = pickle.load(file)
    # Conversion of names to string AND Title REQUIRED
    beer_list = beer_list['name'].astype(str).str.title()
    beer_list = beer_list.to_list()
    return name if name in beer_list else 'Invalid Name'


def get_most_similar_beers(name, n_beers=5, similarity='cosine'):
    """
    Check that name is valid
    """
    if check_name(name) != name:
        return {'response': f'{name} is not a valid name'}

    # Import the model as a pickle
    with open("assets/dataframe.pkl", "rb") as file:
        working_df = pickle.load(file)

    # Get similarity scores between beers
    # To extract for function and to be executed only once
    if similarity == 'cosine':
        with open("assets/cosine.pkl", "rb") as file:
            kernel = pickle.load(file)
    elif similarity == 'sigmoid':
        with open("assets/sigmoid.pkl", "rb") as file:
            kernel = pickle.load(file)
    elif similarity == 'linear':
        with open("assets/linear.pkl", "rb") as file:
            kernel = pickle.load(file)
    results = get_recommendations(working_df, name,
                      sim_matrix=kernel, n_recomm=n_beers)
    results = results[['name', 'brewery', 'style', 'abv', 'min ibu', 'max ibu']]

    return results.to_dict()

def get_most_similar_beers_ibu_abv(name,
                           ibu,
                           abv,
                           input_country=None,
                           n_beers=5, 
                           similarity='cosine'):
    """
    Main function to return beer from the API interrogation
    Possibility to adjust, alcohol, bitterness (IBU), country of origin
    as well as number of recommendations and type of algorithm
    """
    if check_name(name) != name:
        return {'response': f'{name} is not a valid name'}

    # Import the model as a pickle
    with open("assets/dataframe.pkl", "rb") as file:
        working_df = pickle.load(file)

    # Get similarity scores between beers
    # To extract for function and to be executed only once
    if similarity == 'cosine':
        with open("assets/cosine.pkl", "rb") as file:
            kernel = pickle.load(file)
    elif similarity == 'sigmoid':
        with open("assets/sigmoid.pkl", "rb") as file:
            kernel = pickle.load(file)
    elif similarity == 'linear':
        with open("assets/linear.pkl", "rb") as file:
            kernel = pickle.load(file)

    # Filter results if IBU or ABV are specified
    if ibu is not None:
        bad_index_ibu = working_df[working_df['max ibu'] > ibu]
        bad_index_ibu = set(bad_index_ibu.index)
    else:
        bad_index_ibu = set()

    if abv is not None:
        bad_index_abv = working_df[working_df['abv'] > abv]
        bad_index_abv = set(bad_index_abv.index)
    else:
        bad_index_abv = set()
    
    bad_idx_countries = bad_country_filter(working_df, input_country)

    bad_indexes = bad_index_abv.union(bad_index_ibu).union(bad_idx_countries)
    # keep current beer position in kernel
    name_position = get_name_index(name, working_df)
    bad_indexes.discard(int(name_position))
    bad_indexes = list(bad_indexes)

    # Get the recommendation
    results = get_recommendations(
        working_df, name,
        sim_matrix=kernel,
        n_recomm=n_beers,
        ignore_index_beers=bad_indexes)

    results = results[['name', 'brewery',
                       'style', 'abv',
                       'min ibu', 'max ibu',
                       'country']]

    return results.to_dict()


def get_similar_style(
        style,
        abv=None,
        ibu=None,
        n_beers=5,
        similarity='cosine'):
    """
    For a given style, return beers close to the average beer
    Possibility to limit the alcohol content and bitterness
    """

    # Import data, preprocess it
    # To extract for function and to be executed only once
    model = BaseModel()
    model.get_data()
    model.set_preprocess_pipeline()
    model.preprocess.fit(model.working_df)
    model.X = model.preprocess.transform(model.working_df)

    # Import the model as a pickle
    with open("assets/dataframe.pkl", "rb") as file:
        working_df = pickle.load(file)

    # Get average features for a given style
    style_df = working_df[working_df['style'] == style]
    style_df = style_df.index
    style_df = model.X[style_df, :]
    style_df = style_df.mean(axis=0).reshape(1,-1)

    # Get similarity scores between beers
    # To extract for function and to be executed only once
    if similarity == 'cosine':
        kernel = cosine_similarity(style_df, model.X)
    elif similarity == 'sigmoid':
        kernel =  sigmoid_kernel(style_df,  model.X)
    elif similarity == 'linear':
        kernel = linear_kernel(style_df, model.X)

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

    # Extract most similar beers after sorting
    score = sorted(
        list(enumerate(kernel[0])), # Verify here
        key=lambda x:x[1],reverse=True)

    # Filter out beers that don't meet ABV and IBU requirements
    if bad_indexes:
        beers_indices = [i[0] for i in score if i[0] not in bad_indexes]
    else:
        beers_indices = [i[0] for i in score]

    # Top 10 most similar beers
    beers_indices = beers_indices[:n_beers]
    results = model.working_df.iloc[beers_indices, :]
    results = results[['name', 'brewery',
                       'style', 'abv',
                       'min ibu', 'max ibu']]

    return results.to_dict()


if __name__ == '__main__':
    # print(check_name('Our Special Ale 2019 (Anchor Christmas Ale)'))
    # print(check_name('Gaffel Kölsch'))
    # print(check_name('abcde') == 'Invalid Name')
    # print(check_name('Longist Trail Ale') == 'Invalid Name')
    print(check_name('Duvel'))
    print(check_name('Budweiser'))
    print(get_most_similar_beers('Amber'))
    print(get_most_similar_beers_ibu_abv('Duvel', ibu=70, abv=6))
    print(get_similar_style('Stout', ibu=70, abv=6))