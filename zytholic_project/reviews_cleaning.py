import pandas as pd
from zytholic_project.reviews_data import BaseModelRev


def reviews_sorted():
    # import of dataset
    dfreviews = pd.read_csv(
        "../raw_data/Beers_Breweries_and_Beer Reviews/reviews.csv")

    # Class instanciate to get the matching beer id columns
    model = BaseModelRev()
    model.get_data()
    dfid = model.working_df['id']
    dfidlist = dfid.to_list()
    dfrev = dfreviews[['beer_id', 'text']].copy()
    dfrev = dfrev[dfrev['beer_id'].isin(dfidlist)]

    # Clean dataset
    dfrev['text'] = dfrev['text'].astype(str)
    dfrev = dfrev[dfrev['text'] != '\xa0\xa0']

    # Concatenated review in each beer id
    dfrev['text'] = dfrev.groupby(['beer_id'])['text'].transform(lambda x: ' '.join(x))
    dfrevclean = dfrev.drop_duplicates()

    # Write the Csv
    dfrevclean.to_csv("raw_data/reviews_top_beer_concatenated.csv", index=False)


if __name__ == '__main__':
    reviews_sorted()
    print('Files saved after reviews sorted')
