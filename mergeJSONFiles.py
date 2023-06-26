import json

# Read the contents of the JSON files
with open('data/hasFrameRelation/hasFrameRelation.json') as file:
    hasFrame_data = json.load(file)

with open('data/closeMatch/closeMatch.json') as file:
    closeMatch_data = json.load(file)

with open('data/sameAs/sameAs.json') as file:
    sameAs_data = json.load(file)

with open('data/inheritsFrom/inheritsFrom.json') as file:
    inheritsFrom_data = json.load(file)

with open('data/hasRole/hasRole.json') as file:
    hasRole_data = json.load(file)

with open('data/hasFrameElement/hasFrameElement.json') as file:
    hasFrameElement_data = json.load(file)

# Combine the JSON data
combined_data = []
for hasFrame_entry in hasFrame_data:
    frame_name = hasFrame_entry['frame_name']
    frame_roles = hasFrame_entry['frame_roles']
    tweet_id = hasFrame_entry['tweet_id']
    tweet_text= hasFrame_entry['text']
    topics = hasFrame_entry['topics']
    tweet_date = hasFrame_entry['date']
    subjectivity = hasFrame_entry['subjectivity']
    polarity = hasFrame_entry['polarity']
    analysis = hasFrame_entry['analysis']
    results = hasFrame_entry['results']['results']['bindings']

    closeMatch_entry = next((entry for entry in closeMatch_data if entry['frame_name'] == frame_name), None)
    sameAs_entry = next((entry for entry in sameAs_data if entry['frame_name'] == frame_name), None)
    inheritsFrom_entry = next((entry for entry in inheritsFrom_data if entry['frame_name'] == frame_name), None)
    hasRole_entry = next((entry for entry in hasRole_data if entry['frame_name'] == frame_name), None)
    hasFrameElement_entry = next((entry for entry in hasFrameElement_data if entry['frame_name'] == frame_name), None)

    closeMatch_results = closeMatch_entry['results']['results']['bindings'] if closeMatch_entry else []
    sameAs_results = sameAs_entry['results']['results']['bindings'] if sameAs_entry else []
    inheritsFrom_results = inheritsFrom_entry['results']['results']['bindings'] if inheritsFrom_entry else []
    hasRole_results = hasRole_entry['results']['results']['bindings'] if hasRole_entry else []
    hasFrameElement_results = hasFrameElement_entry['results']['results']['bindings'] if hasFrameElement_entry else []

    combined_entry = {
        'frame_name': frame_name,
        'frame_roles': frame_roles,
        'tweet_id': tweet_id,
        'text': tweet_text,
        'topics': topics,
        'date': tweet_date,
        'subjectivity': subjectivity,
        'polarity': polarity,
        'analysis': analysis,
        'results': {
            'hasFrameRelation': results,
            'closeMatch': closeMatch_results,
            'sameAs': sameAs_results,
            'inheritsFrom': inheritsFrom_results,
            'hasRole': hasRole_results,
            'hasFrameElement': hasFrameElement_results
        }
    }

    combined_data.append(combined_entry)

# Write the combined JSON data to a file
with open('data/combined.json', 'w') as file:
    json.dump(combined_data, file, indent=4)
