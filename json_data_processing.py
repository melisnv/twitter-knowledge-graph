import pandas as pd
import json
import os


def process_json_data(json_dir):
    '''
    This function creates a dataframe from JSON files
    :param json_dir: file location of the JSON files
    :return: a dataframe created by merging JSON files
    '''

    # creating an empty list to store the dataframes
    df_list = []

    for filename in os.listdir(json_dir):
        # checking if the file is a JSON file
        if filename.endswith('.json'):
            # loading the JSON data
            with open(os.path.join(json_dir, filename), 'r', encoding='ISO-8859-1') as f:
                data = json.load(f)
            # converting the dictionary to a DataFrame and append it to the list
            df_list.append(pd.DataFrame.from_dict(data))

    # concatenating all dataframes in the list into one dataframe
    data = pd.concat(df_list, ignore_index=True)

    return data

