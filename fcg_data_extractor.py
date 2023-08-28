import csv
import requests
import json

fcg_url = "http://127.0.0.1:1170/extract-frames"
headers = {
    'Content-Type': 'application/json',
}

def extract_fcg_data(csv_path):
    '''
    This function sends a call to FCG Editor for extracting the semantic frames
    and saves the output result as JSON file.
    :param csv_path: The file location of processed Twitter data
    :return: An output from FCG Editor contains semantic frames of Twitter data
    '''
    fcg_output_list = []

    with open(csv_path, 'r', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tweet_text = row['cleaned_text']
            tweet_id = row['id']
            tweet_date = row['created_at']
            tweet_topic = row['topic']
            tweet_subjectivity = row['subjectivity']
            tweet_polarity = row['polarity']
            tweet_analysis = row['analysis']

            data = {
                "utterance": tweet_text,
                "package": "propbank-grammar",
                "grammar": "*propbank-grammar*",
                "timeout": 100,
            }

            response = requests.post(fcg_url, headers=headers, json=data)
            try:
                fcg_output = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                print("Error decoding JSON response. Skipping to the next utterance.")
                continue

            # adding tweet ID to output
            fcg_output['id'] = tweet_id

            # adding tweet topic to output
            fcg_output['topic'] = tweet_topic

            # adding tweet text to output
            fcg_output['text'] = tweet_text

            # adding tweet date to output
            fcg_output['date'] = tweet_date

            # adding tweet subjectivity to output
            fcg_output['subjectivity'] = tweet_subjectivity

            # adding tweet polarity to output
            fcg_output['polarity'] = tweet_polarity

            # adding tweet analysis to output
            fcg_output['analysis'] = tweet_analysis

            # append the fcg_output to the list
            fcg_output_list.append(fcg_output)

    # saving the fcg_output_list as a JSON file
    with open('./data/fcg_output.json', 'w') as f:
        json.dump(fcg_output_list, f, indent=4)


if __name__ == "__main__":
    csv_path = './data/twitter_data.csv'
    extract_fcg_data(csv_path)
