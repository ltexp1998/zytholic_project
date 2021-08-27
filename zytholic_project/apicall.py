import pandas as pd

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
    
    
if __name__ == '__main__':
    print(check_name('Our Special Ale 2019 (Anchor Christmas Ale)'))
    print(check_name('Gaffel Kölsch'))
    print(check_name('abcde') == 'Invalid Name')
    print(check_name('Longist Trail Ale') == 'Invalid Name')
