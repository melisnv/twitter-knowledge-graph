import pandas as pd
import json
import os

# defining the directory where the JSON files are located
json_dir = 'data/'

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
# saving the DataFrame as a CSV file
data.to_csv('data/twitter_data.csv', index=False)
