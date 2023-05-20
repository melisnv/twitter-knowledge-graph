import json

# Load the first JSON file
with open('data/hasFrameRelation/hasFrameRelation.json') as f1:
    data1 = json.load(f1)

# Load the second JSON file
with open('data/closeMatch/closeMatch.json') as f2:
    data2 = json.load(f2)

# Merge the "results" section
merged_results = {
    'distinct': data1['results']['distinct'],
    'ordered': data1['results']['ordered'],
    'bindings': data1['results']['bindings'] + data2['results']['bindings']
}

# Create the merged JSON object
merged_json = {
    'head': {
        'link': [],
        'vars': data1['head']['vars'] + data2['head']['vars']
    },
    'results': merged_results
}

# Save the merged JSON file
with open('data/merged.json', 'w') as outfile:
    json.dump(merged_json, outfile, indent=4)
