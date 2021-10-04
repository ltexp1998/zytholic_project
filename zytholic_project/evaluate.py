import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import sigmoid_kernel, cosine_similarity, linear_kernel


def get_name_index(name, df):
    """From a name of a beer, find it index in the dataframe"""
    # Dataframe to get index of a given beer
    temp = df[["name"]].copy()
    temp.reset_index(drop=True, inplace=True)  # removes old index
    index = temp.reset_index()  # get lines numbers as index column
    position = index[index["name"] == name]["index"]
    return position


def get_recommendations(
    df, name, sim_matrix=None, n_recomm=10, ignore_index_beers=None
):
    """
    Uses similarity distance using sim_matrix to return the 10 closest beers
    to the "name" input inside the specified DF
    """
    position = get_name_index(name, df)

    # Extract most similar beers after sorting
    score = sorted(
        list(enumerate(sim_matrix[position][0])),  # Verify here
        key=lambda x: x[1],
        reverse=True,
    )
    indices = score

    if ignore_index_beers:
        beers_indices = [i[0] for i in indices if i[0] not in ignore_index_beers]

    else:
        beers_indices = [i[0] for i in indices]
    # Top 10 most similar beers
    beers_indices = beers_indices[: n_recomm + 1]
    return df.iloc[beers_indices, :]


def evaluate_proximity(
    df,
    n_recomm=10,
    tests=10,
    sim_matrix=None,
):
    """
    For each style in a give dataframe, return percentage of recommendations
    that have the same style and the number of items of said style in the DF
    """
    df_styles = df["style"].value_counts()

    results = []
    mod_list = []
    # Explore each style
    for st in df_styles.index:
        # Get a few random samples
        samples = df[df["style"] == st]["name"]
        samples = samples.sample(min(tests, len(samples)))

        percent = []
        mod = {}
        for name in samples:
            # calculate content based similarity for each sample
            res = get_recommendations(df, name, sim_matrix, n_recomm)
            # Get percentage of matching style for each sample
            matching_percent = res[res["style"] == st].shape[0] / res.shape[0] * 100
            percent.append(matching_percent)

            # count which are the most suggested labels
            dict_count = res.value_counts("style").to_dict()
            for lab, val in dict_count.items():
                value = mod.get(lab, 0)
                mod[lab] = value + val

        # average for each style
        style_result = np.array(percent).mean()
        results.append(style_result)

        val_counts = pd.Series(mod).sort_values(ascending=False).reset_index()
        mod_list.append(val_counts.iloc[0, 0])

    final_style = df_styles.reset_index()
    final_style["matching_percent"] = results
    final_style["mod"] = mod_list
    return final_style


def test_prediction(model, n_recomm=10, similarity="cosine"):

    if similarity == "cosine":
        kernel = cosine_similarity(model.X_test_proc, model.X_train_proc)
    if similarity == "sigmoid":
        kernel = sigmoid_kernel(model.X_test_proc, model.X_train_proc)
    if similarity == "linear":
        kernel = linear_kernel(model.X_test_proc, model.X_train_proc)

    matching_results = []
    substyles = []
    # Predict the closest beers in reference dataset
    for idx in range(kernel.shape[0]):
        distances = kernel[idx, :]
        sorted_distances = sorted(
            list(enumerate(distances)), key=lambda x: x[1], reverse=True
        )
        # get the top n predictions
        closest_items = sorted_distances[0 : n_recomm + 1]
        beers_indices = [i[0] for i in closest_items]

        # check original_style == predict_style percentage
        original_style = model.X_test["style"].iloc[idx]
        propositions = model.X_train.iloc[beers_indices, :]

        matching_percent = (
            propositions[propositions["style"] == original_style].shape[0]
            / propositions.shape[0]
            * 100
        )
        matching_results.append(matching_percent)

        # compare substyle matching
        original_substyle = model.X_test.iloc[idx, -7:]
        comp = propositions.iloc[:, -7:]
        substyle_match = ((original_substyle == comp).sum() / comp.shape[0]).min()
        substyles.append(substyle_match * 100)

        # if (original_style == 'Stout') & (model.X_test["milk"].iloc[idx] == 1): ipdb.set_trace()

    results = model.X_test.copy()
    results["matching_percent"] = matching_results
    results["matching_substyle"] = substyles
    return results
