import json


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def merge_data(combined_entry, entry_data, key_name):
    entry = next((entry for entry in entry_data if entry['frame_name'] == combined_entry['frame_name']), None)
    results = entry['results']['results']['bindings'] if entry else []
    combined_entry['results'][key_name] = results


def merge_json_files():
    combined_data = []

    hasFrame_data = load_json_file('data/hasFrameRelation.json')
    closeMatch_data = load_json_file('data/closeMatch.json')
    sameAs_data = load_json_file('data/sameAs.json')

    inheritsFrom_data = load_json_file('data/inheritsFrom.json')
    hasRole_data = load_json_file('data/hasRole.json')
    hasFrameElement_data = load_json_file('data/hasFrameElement.json')

    hasComment_data = load_json_file('data/hasComment.json')
    hasInchoative_data = load_json_file('data/hasInchoative.json')
    isCausativeOf_data = load_json_file('data/isCausativeOf.json')

    isInchoativeOf_data = load_json_file('data/isInchoativeOf.json')
    isPerspectivizedIn_data = load_json_file('data/isPerspectivizedIn.json')
    narrowerMatch_data = load_json_file('data/narrowerMatch.json')

    perspectiveOn_data = load_json_file('data/perspectiveOn.json')
    precedes_data = load_json_file('data/precedes.json')
    seeAlso_data = load_json_file('data/seeAlso.json')

    for hasFrame_entry in hasFrame_data:
        combined_entry = {
            'frame_name': hasFrame_entry['frame_name'],
            'frame_roles': hasFrame_entry['frame_roles'],
            'tweet_id': hasFrame_entry['tweet_id'],
            'text': hasFrame_entry['text'],
            'topics': hasFrame_entry['topics'],
            'date': hasFrame_entry['date'],
            'subjectivity': hasFrame_entry['subjectivity'],
            'polarity': hasFrame_entry['polarity'],
            'analysis': hasFrame_entry['analysis'],
            'results': {}
        }

        merge_data(combined_entry, closeMatch_data, 'closeMatch')
        merge_data(combined_entry, sameAs_data, 'sameAs')
        merge_data(combined_entry, inheritsFrom_data, 'inheritsFrom')
        merge_data(combined_entry, hasRole_data, 'hasRole')
        merge_data(combined_entry, hasFrameElement_data, 'hasFrameElement')
        merge_data(combined_entry, hasComment_data, 'hasComment')
        merge_data(combined_entry, hasInchoative_data, 'hasInchoative')
        merge_data(combined_entry, isCausativeOf_data, 'isCausativeOf')
        merge_data(combined_entry, isInchoativeOf_data, 'isInchoativeOf')
        merge_data(combined_entry, isPerspectivizedIn_data, 'isPerspectivizedIn')
        merge_data(combined_entry, narrowerMatch_data, 'narrowerMatch')
        merge_data(combined_entry, perspectiveOn_data, 'perspectiveOn')
        merge_data(combined_entry, precedes_data, 'precedes')
        merge_data(combined_entry, seeAlso_data, 'seeAlso')

        combined_data.append(combined_entry)

    with open('data/combined_outputs.json', 'w') as file:
        json.dump(combined_data, file, indent=4)


if __name__ == "__main__":
    merge_json_files()
