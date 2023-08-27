import json

# reading the contents of the JSON files
with open('data/lastQueryResults/hasFrameRelation2000.json') as file:
    hasFrame_data = json.load(file)

with open('data/lastQueryResults/closeMatch2000.json') as file:
    closeMatch_data = json.load(file)

with open('data/lastQueryResults/sameAs2000.json') as file:
    sameAs_data = json.load(file)

with open('data/lastQueryResults/inheritsFrom2000.json') as file:
    inheritsFrom_data = json.load(file)

with open('data/lastQueryResults/hasRole2000.json') as file:
    hasRole_data = json.load(file)

with open('data/lastQueryResults/hasFrameElement2000.json') as file:
    hasFrameElement_data = json.load(file)

with open('data/lastQueryResults/hasComment2000.json') as file:
    hasComment_data = json.load(file)

with open('data/hasInchoative/hasInchoative.json') as file:
    hasInchoative_data = json.load(file)

with open('data/isCausativeOf/isCausativeOf.json') as file:
    isCausativeOf_data = json.load(file)

with open('data/isInchoativeOf/isInchoativeOf.json') as file:
    isInchoativeOf_data = json.load(file)

with open('data/isPerspectivizedIn/isPerspectivizedIn.json') as file:
    isPerspectivizedIn_data = json.load(file)

with open('data/narrowerMatch/narrowerMatch.json') as file:
    narrowerMatch_data = json.load(file)

with open('data/perspectiveOn/perspectiveOn.json') as file:
    perspectiveOn_data = json.load(file)

with open('data/precedes/precedes.json') as file:
    precedes_data = json.load(file)

with open('data/seeAlso/seeAlso.json') as file:
    seeAlso_data = json.load(file)

# merging the JSON data
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
    hasComment_entry = next((entry for entry in hasComment_data if entry['frame_name'] == frame_name), None)


    hasInchoative_entry = next((entry for entry in hasInchoative_data if entry['frame_name'] == frame_name), None)
    isCausativeOf_entry = next((entry for entry in isCausativeOf_data if entry['frame_name'] == frame_name), None)
    isInchoativeOf_entry = next((entry for entry in isInchoativeOf_data if entry['frame_name'] == frame_name), None)
    isPerspectivizedIn_entry = next((entry for entry in isPerspectivizedIn_data if entry['frame_name'] == frame_name), None)
    narrowerMatch_entry = next((entry for entry in narrowerMatch_data if entry['frame_name'] == frame_name), None)
    precedes_entry = next((entry for entry in precedes_data if entry['frame_name'] == frame_name), None)
    perspectiveOn_entry = next((entry for entry in perspectiveOn_data if entry['frame_name'] == frame_name), None)
    seeAlso_entry = next((entry for entry in seeAlso_data if entry['frame_name'] == frame_name), None)

    closeMatch_results = closeMatch_entry['results']['results']['bindings'] if closeMatch_entry else []
    sameAs_results = sameAs_entry['results']['results']['bindings'] if sameAs_entry else []
    inheritsFrom_results = inheritsFrom_entry['results']['results']['bindings'] if inheritsFrom_entry else []
    hasRole_results = hasRole_entry['results']['results']['bindings'] if hasRole_entry else []
    hasFrameElement_results = hasFrameElement_entry['results']['results']['bindings'] if hasFrameElement_entry else []
    hasComment_results = hasComment_entry['results']['results']['bindings'] if hasComment_entry else []

    hasInchoative_results = hasInchoative_entry['results']['results']['bindings'] if hasInchoative_entry else []
    isCausativeOf_results = isCausativeOf_entry['results']['results']['bindings'] if isCausativeOf_entry else []
    isInchoativeOf_results = isInchoativeOf_entry['results']['results']['bindings'] if isInchoativeOf_entry else []
    isPerspectivizedIn_results = isPerspectivizedIn_entry['results']['results']['bindings'] if isPerspectivizedIn_entry else []
    narrowerMatch_results = narrowerMatch_entry['results']['results']['bindings'] if narrowerMatch_entry else []
    precedes_results = precedes_entry['results']['results']['bindings'] if precedes_entry else []
    perspectiveOn_results = perspectiveOn_entry['results']['results']['bindings'] if perspectiveOn_entry else []
    seeAlso_results = seeAlso_entry['results']['results']['bindings'] if seeAlso_entry else []

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
            'hasFrameElement': hasFrameElement_results,
            'hasComment': hasComment_results,

            'hasInchoative': hasInchoative_results,
            'isCausativeOf': isCausativeOf_results,
            'isInchoativeOf': isInchoativeOf_results,
            'isPerspectivizedIn': isPerspectivizedIn_results,
            'narrowerMatch': narrowerMatch_results,
            'precedes': precedes_results,
            'perspectiveOn': perspectiveOn_results,
            'seeAlso': seeAlso_results
        }
    }

    combined_data.append(combined_entry)

# saving the combined JSON data to a file
with open('data/combined_outputs.json', 'w') as file:
    json.dump(combined_data, file, indent=4)
