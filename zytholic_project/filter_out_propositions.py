import numpy as np
import pandas as pd


def filter_bad_countries(dataframe, country=None):
    """From a dataframe, return a list of all indexes where the country
    doesn't match the one specified in the function call"""
    if country is None:
        return list()
    bad_indices = np.where(dataframe["country"] != country)[0]
    return bad_indices.tolist()


def filter_bad_ibu(dataframe, ibu: float) -> list:
    """Returns indexes of beers that don't match the specified IBU"""
    bad_index_ibu = []
    if ibu is not None:
        bad_index_ibu = dataframe[dataframe["max ibu"] > ibu]
        bad_index_ibu = list(bad_index_ibu.index)
    return bad_index_ibu


def filter_bad_abv(dataframe: pd.DataFrame, abv: float) -> list:
    """Returns indexes of beers that are above the specified ABV"""
    bad_index_abv = []
    if abv is not None:
        bad_index_abv = dataframe[dataframe["abv"] > abv]
        bad_index_abv = list(bad_index_abv.index)
    return bad_index_abv


def list_bad_ibu_abv_country(dataframe, abv, ibu, input_country):
    """
    Returns all the beer indexes that should be ignored based on user inputs.
    """
    bad_index_ibu = filter_bad_ibu(dataframe, ibu)
    bad_index_abv = filter_bad_abv(dataframe, abv)
    bad_idx_countries = filter_bad_countries(dataframe, input_country)
    # concatenates list and keeps unique elements
    return set(bad_index_abv + bad_index_ibu + bad_idx_countries)