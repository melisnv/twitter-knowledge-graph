import csv
import rdflib
import requests
import json
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
with open('data/sample_tweet_data.csv', 'r', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # extract the text of the tweet from the 'text' column
        tweet_text = row['cleaned_text']
        tweet_id = row['id']
        tweet_date = row['created_at']
        tweet_topic = row['topic']
        tweet_subjectivity = row['Subjectivity']
        tweet_polarity = row['Polarity']
        tweet_analysis = row['Analysis']

        # the data dictionary for the API call
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

        # adding tweet text to output
        fcg_output['text'] = tweet_text
        output_dict[tweet_text] = fcg_output

        # adding tweet date to output
        fcg_output['date'] = tweet_date
        output_dict[tweet_date] = fcg_output

        # adding tweet subjectivity to output
        fcg_output['subjectivity'] = tweet_subjectivity
        output_dict[tweet_subjectivity] = fcg_output

        # adding tweet polarity to output
        fcg_output['polarity'] = tweet_polarity
        output_dict[tweet_polarity] = fcg_output

        # adding tweet analysis to output
        fcg_output['analysis'] = tweet_analysis
        output_dict[tweet_analysis] = fcg_output

        # appending the fcg_output to the list
        fcg_output_list.append(fcg_output)


# writing the list to a JSON file
with open('data/hasComment/fcg_output_hasComment.json', 'w') as outfile:
    json.dump(fcg_output_list, outfile)


# creating an list to store the results of all frames from all tweets
combined_results_list = []

for output in fcg_output_list:
    if output.get("frameSet") is not None and output["frameSet"] is not None:
        frame_set = output["frameSet"]
        tweet_id = output["id"]
        tweet_text = output["text"]
        tweet_date = output["date"]
        tweet_polarity = output["polarity"]
        tweet_analysis = output["analysis"]
        tweet_subjectivity = output["subjectivity"]
        topic_list = output['topic'].split(', ')  # make topics list
        tweet_frames = {}

        results_list = []  # Create an empty list to store the results for each frame

        for frame in frame_set:
            frame_name = frame["frameName"]
            roles = frame["roles"]
            frame_roles = {}

            for role in roles:
                role_name = role["role"]
                role_string = role["string"]

                # Store the role and string in the frame_roles dictionary
                if role_name in frame_roles:
                    frame_roles[role_name].append(role_string)
                else:
                    frame_roles[role_name] = [role_string]

                print(
                    f"Date: {tweet_date}, Tweet ID: {tweet_id}, Tweet : {tweet_text},"
                    f" Frame: {frame_name}, Role: {role_name}, String: {role_string}, Topic: {topic_list},"
                    f"Subjectivity : {tweet_subjectivity}, Polarity : {tweet_polarity}, Analysis : {tweet_analysis}")


            # the SPARQL query to retrieve information about the frame from Framester
            sparql_template = r'''
            PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
            SELECT DISTINCT ?frame ?comment
            WHERE {{
                ?frame a tbox:Frame ;
                     rdfs:comment ?comment ;
                    skos:closeMatch ?closeFrames .
                FILTER regex(str(?closeFrames), "{frame_name}")
            }}
            '''

            sparql_query = sparql_template.format(frame_name=frame_name, sent_number=1)
            sparql = SPARQLWrapper("http://etna.istc.cnr.it/framester2/sparql")
            # TODO: Try agent
            #sparql = SPARQLWrapper(sparql_endpoint, agent=agent)
            sparql.setTimeout(300)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)

            sparql.addParameter('User-Agent',
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
            results = sparql.query().convert()

            results_with_frame_name = {
                "frame_name": frame_name,
                "tweet_id": tweet_id,
                "text": tweet_text,
                "date": tweet_date,
                "subjectivity": tweet_subjectivity,
                "polarity": tweet_polarity,
                "analysis": tweet_analysis,
                "frame_roles": frame_roles,
                "topics": topic_list,
                "results": results
            }
            results_list.append(results_with_frame_name)  # appending the results to the results_list

        # appending the results_list to the combined_results_list
        combined_results_list.extend(results_list)
        print(combined_results_list)

# writing the combined_results_list to a single JSON file
with open('data/hasComment/hasComment.json', 'w') as f:
    json.dump(combined_results_list, f, indent=4)
