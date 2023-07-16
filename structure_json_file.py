import json

input_file = "data/denemehasFrameRelation/fcg_output_denemehasFrameRelation.json"
output_file = "filtered_json.json"
target_id = "1457383855896162305"
max_tweets = 2000

tweets = []

with open(input_file) as file:
    data = json.load(file)

for tweet in data:
    if tweet["id"] == target_id:
        break
    tweets.append(tweet)
    if len(tweets) >= max_tweets:
        break

with open(output_file, "w") as file:
    json.dump(tweets, file)
