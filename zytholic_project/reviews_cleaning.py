import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from zytholic_project.reviews_data import BaseModelRev
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def reviews_sorted():
    # import of dataset
    dfreviews = pd.read_csv("../raw_data/Beers_Breweries_and_Beer Reviews/reviews.csv")

    # Class instanciate to get the matching beer id columns
    model = BaseModelRev()
    model.get_data()
    dfid = model.working_df["id"]
    dfidlist = dfid.to_list()
    dfrev = dfreviews[["beer_id", "text"]].copy()
    dfrev = dfrev[dfrev["beer_id"].isin(dfidlist)]
    # Drop reviews with no text
    dfrev["text"] = dfrev["text"].astype(str)
    dfrev = dfrev[dfrev["text"] != "\xa0\xa0"]

    # Concatenated review in each beer id
    dfrev["text"] = dfrev.groupby(["beer_id"])["text"].transform(lambda x: " ".join(x))
    dfrevclean = dfrev.drop_duplicates()

    # Write the Csv
    dfrevclean.to_csv("raw_data/reviews_top_beer_concatenated.csv", index=False)


if __name__ == "__main__":
    reviews_sorted()
    print("Files saved after reviews sorted")


def preprocessing(text):

    # Transform text to English words

    for punctuation in string.punctuation:
        text = text.replace(punctuation, " ")
    # Lowercased the text
    lowercased = text.lower()
    # Dropping all the numbers
    clean = "".join([i for i in lowercased if not i.isdigit()])
    # Empty review are filled with \xa0
    replaced = clean.replace("\xa0", "")

    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(replaced)
    text = [w for w in word_tokens if not w in stop_words]

    lemmatizer = nltk.stem.WordNetLemmatizer()
    text = " ".join([lemmatizer.lemmatize(token) for token in text]).strip()
    # Drop the punctuation that the first function miss
    garbage = "~`!@#$%^&*()_-+={[}]|\:;'<,>.?/"
    text = "".join([char for char in text if char not in garbage])

    return text


def reviews_featuring(dataframe):

    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words="english", token_pattern="[a-z]+\w*", min_df=20)

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(dataframe["text"])

    # Fit the SVD to create 10 new features
    svd = TruncatedSVD(n_components=10, n_iter=10, random_state=42)
    svd.fit(tfidf_matrix)
    feat = svd.transform(tfidf_matrix)
    # Transform the new features into a dataframe
    feat = pd.DataFrame(feat)
    result = pd.concat([dataframe, feat], axis=1, join="inner")
    return result
