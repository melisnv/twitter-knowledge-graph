import json

# Read the contents of the JSON files
with open('data/hasFrameRelation/hasFrameRelation.json') as file:
    hasFrame_data = json.load(file)

with open('data/closeMatch/closeMatch.json') as file:
    closeMatch_data = json.load(file)

# Combine the JSON data
combined_data = []
for hasFrame_entry in hasFrame_data:
    frame_name = hasFrame_entry['frame_name']
    frame_roles = hasFrame_entry['frame_roles']
    tweet_id = hasFrame_entry['tweet_id']
    topics = hasFrame_entry['topics']
    results = hasFrame_entry['results']['results']['bindings']
    closeMatch_entry = next((entry for entry in closeMatch_data if entry['frame_name'] == frame_name), None)
    if closeMatch_entry:
        closeMatch_results = closeMatch_entry['results']['results']['bindings']
        combined_entry = {
            'frame_name': frame_name,
            'tweet_id': tweet_id,
            'frame_roles' : frame_roles,
            'topics': topics,
            'results': {
                'hasFrame': results,
                'closeMatch': closeMatch_results
            }
        }
        combined_data.append(combined_entry)

# Write the combined JSON data to a file
with open('data/combined.json', 'w') as file:
    json.dump(combined_data, file, indent=4)
