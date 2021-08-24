import pandas as pd
import ipdb

def style_rename():
    # importation des datasets
    top_beer_info = pd.read_csv(
        'raw_data/top-beer-information/top_beer_information.csv'
        )
    top_beer_info.columns = [x.lower() for x in top_beer_info.columns]
    top_beer_info['name'] = top_beer_info['name'].astype(str)
    top_beer_info['brewery'] = top_beer_info['brewery'].astype(str)
    
    beers = pd.read_csv(
       'raw_data/Beers_Breweries_and_Beer Reviews/beers.csv'
    )
    beers.name = beers.name.astype(str)
    
    # importation du fichier de corresponance des styles
    style_xls = pd.read_excel('assets/style_convert.xlsx')
    style_xls.to_csv("raw_data/style_rename.csv")

    style_csv = pd.read_csv('raw_data/style_rename.csv')
    style_csv.drop(columns='Unnamed: 0', inplace=True)
    style_csv.set_index('Dataset style', inplace=True)
    style_csv = style_csv.iloc[1:, :]

    # creation d'un dict pour replace de la correspondance
    style_dict = style_csv.to_dict()
    style_dict = style_dict['Unnamed: 1']

    # uniformaisation des styles sur les datasets
    beers['style'].replace(style_dict, inplace=True)
    top_beer_info['style'].replace(style_dict, inplace=True)
    #ipdb.set_trace()

    # exportation en csv des datasets modifiés
    top_beer_info.to_csv('raw_data/top_beer_info_style_renamed.csv')
    beers.to_csv('raw_data/beers_style_renamed.csv')
    

if __name__ == '__main__':
        #ipdb.set_trace()
        style_rename()
        print('Files saved after style renaming')
