import pandas as pd

def style_rename():
    # importation des datasets

    top_beer_info = pd.read_csv(
        '/Users/ltexp1998/code/ltexp1998/zytholic_project/raw_data/top-beer-information/top_beer_information.csv')

    beers = pd.read_csv(
        '/Users/ltexp1998/code/ltexp1998/zytholic_project/raw_data/Beers_Breweries_and_Beer Reviews/beers.csv'
    )

    # importation du fichier de corresponance des styles

    style_csv = pd.read_csv(
        '/Users/ltexp1998/code/ltexp1998/zytholic_project/raw_data/style_rename.csv'
    )
    style_csv.drop(columns='Unnamed: 0', inplace=True)
    style_csv.set_index('Dataset style', inplace=True)
    style_csv.drop('Original', 0, inplace=True)

    # creation d'un dict pour replace de la correspondance
    
    style_dict = style_csv.to_dict()
    style_dict = style_dict['Unnamed: 1']

    # uniformaisation des styles sur les datasets

    beers['style'].replace(style_dict, inplace=True)
    top_beer_info['Style'].replace(style_dict, inplace=True)

    # exportation en csv des datasets modifiés

    top_beer_info.to_csv('../raw_data/top_beer_info_style_renamed.csv')
    beers.to_csv('../raw_data/beers_style_renamed.csv')
