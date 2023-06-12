import csv
import rdflib
import requests
import json
import codecs

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal, OWL
from rdflib.namespace import RDF, RDFS, XSD

fcg_url = "http://127.0.0.1:1170/extract-frames"

headers = {
    'Content-Type': 'application/json',
}

fcg_output_list = []
output_dict = {}

# open the data.csv file in read mode
with open('data/twitter_data.csv', 'r', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # extract the text of the tweet from the 'text' column
        tweet_text = row['cleaned_text']
        tweet_id = row['id']
        tweet_topic = row['topic']

        # create the data dictionary for the API call
        data = {
            "utterance": tweet_text,
            "package": "propbank-grammar",
            "grammar": "*propbank-grammar*",
            "timeout": 100,
        }

        # make the API call to extract frames for the tweet text
        response = requests.post(fcg_url, headers=headers, json=data)
        print(response.status_code)  # Print the status code of the response
        print(response.text)  # Print the response text

        try:
            fcg_output = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON response. Skipping to the next utterance.")
            continue

        # adding tweet ID to output
        fcg_output['id'] = tweet_id
        output_dict[tweet_id] = fcg_output

        # adding tweet topic to output
        fcg_output['topic'] = tweet_topic
        output_dict[tweet_topic] = fcg_output

        # append the fcg_output to the list
        fcg_output_list.append(fcg_output)

        # print the frames extracted for the tweet text
        print(fcg_output)

# write the list to a JSON file
with open('data/twitterdata_fcg_output.json', 'w') as outfile:
    json.dump(fcg_output_list, outfile)
