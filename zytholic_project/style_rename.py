import pandas as pd


def style_rename():
    # importation des datasets
    top_beer_info = pd.read_csv(
        "../raw_data/top-beer-information/top_beer_information.csv"
    )
    top_beer_info.columns = [x.lower() for x in top_beer_info.columns]
    top_beer_info["name"] = top_beer_info["name"].astype(str)
    top_beer_info["brewery"] = top_beer_info["brewery"].astype(str)

    beers = pd.read_csv("../raw_data/Beers_Breweries_and_Beer Reviews/beers.csv")
    beers.name = beers.name.astype(str)

    # importation du fichier de corresponance des styles
    style_xls = pd.read_excel("../assets/style_convert.xlsx")
    style_xls.set_index("Dataset style", inplace=True)
    style_xls = style_xls.iloc[1:, :]

    # creation d'un dict pour replace de la correspondance
    style_dict = style_xls.to_dict()
    style_dict = style_dict["Unnamed: 1"]

    # uniformaisation des styles sur les datasets
    beers["style"].replace(style_dict, inplace=True)
    top_beer_info["style"].replace(style_dict, inplace=True)

    # exportation en csv des datasets modifiés
    top_beer_info.to_csv("../raw_data/top_beer_info_style_renamed.csv", index=False)
    beers.to_csv("../raw_data/beers_style_renamed.csv", index=False)


if __name__ == "__main__":
    style_rename()
    print("Files saved after style renaming")
