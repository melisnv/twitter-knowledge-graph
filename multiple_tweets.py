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
        tweet_text = row['text']
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
        fcg_output = json.loads(response.text)

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
with open('fcg_output.json', 'w') as outfile:
    json.dump(fcg_output_list, outfile)


# an RDF graph
g = Graph()

# defining namespaces for Framester and WebVOWL
fv = Namespace('https://w3id.org/framester/ontology/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

tweets_dict = {}

for output in fcg_output_list:
    if output.get("frameSet") is not None and output["frameSet"] is not None:
        frame_set = output["frameSet"]
        tweet_id = output["id"]
        topic_list = output['topic'].split(', ') # make topics list
        tweet_frames = {}

        for frame in frame_set:
            frame_name = frame["frameName"]
            roles = frame["roles"]
            frame_roles = {}

            for role in roles:
                role_name = role["role"]
                role_string = role["string"]
                frame_roles[role_name] = role_string
                print(f"Tweet ID: {tweet_id}, Frame: {frame_name}, Role: {role_name}, String: {role_string}, Topic : {topic_list}" )

            tweet_frames[frame_name] = frame_roles

            # the SPARQL query to retrieve information about the frame from Framester
            sparql_template = r'''
            PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
            SELECT DISTINCT ?frame ?name ?matchedFrames
            WHERE {{
            ?frame a tbox:Frame ;
                tbox:frame_name ?name ;
                rdfs:comment ?def ;
                skos:closeMatch ?matchedFrames ;
                skos:closeMatch ?closeFrames .
            FILTER regex(str(?closeFrames), "{frame_name}")
            }}
            '''

            sparql_query = sparql_template.format(frame_name=frame_name, sent_number=1)
            sparql = SPARQLWrapper("http://etna.istc.cnr.it/framester2/sparql")
            sparql.setTimeout(300)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            #print("RESULTS:", results)
            with open('results.json', 'w') as f:
                json.dump(results, f)

            g_all_tweets = rdflib.Graph()

            for result in results['results']['bindings']:
                frame_uri = rdflib.URIRef(result['frame']['value'])
                frameName = result['name']['value']

                tweet_uri = rdflib.URIRef(tweet_id)

                print("frame_roles: ", frame_roles)
                arguments = {}
                for role, value in frame_roles.items():
                    if role.startswith('arg'):
                        arg_num = role[3:]  # extract the argument number
                        arguments[f"arg{arg_num}"] = value

                for arg, val in arguments.items():
                    arg_uri = rdflib.URIRef(arg)
                    arg_val = Literal(val)

                matchedFrames_uri = rdflib.URIRef(result['matchedFrames']['value'])
                matchedFrameName = result['matchedFrames']['value'].split("/")[-1]

                # Add the frame and matched frames to the tweet frames dictionary
                if frame_name not in tweet_frames:
                    tweet_frames[frame_name] = {}
                tweet_frames[frame_name]['matchedFrames'] = matchedFrameName

                # Add the frame and matched frames to the RDF graph
                # Tweet
                g.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
                g.add((tweet_uri, RDFS.label, Literal(tweet_id)))

                # Tweet Topic (About)
                for topic in topic_list:
                    topic_uri = rdflib.URIRef(topic)
                    g.add((topic_uri, RDF.type, URIRef('http://example.com/Topic')))
                    g.add((topic_uri, RDFS.label, Literal(topic_uri)))
                    g.add((topic_uri, URIRef('http://example.com/isAbout'), tweet_uri))

                # Frame
                g.add((frame_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/tbox/Frame')))
                g.add((frame_uri, RDFS.label, Literal(frameName)))
                g.add((tweet_uri, URIRef('http://example.com/hasFrame'), frame_uri))

                # Argument
                #g.add((arg_uri, RDF.type, URIRef('http://example.com/Argument')))
                g.add((arg_uri, RDF.type, URIRef(f'http://example.com/{arg_uri}'))) # arg0, arg1, arg2 etc.
                g.add((arg_uri, RDFS.label, Literal(arg_val)))
                g.add((tweet_uri, URIRef('http://example.com/hasArgument'), arg_uri))

                # matched Frames (skos)
                g.add(
                    (matchedFrames_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/tbox/hasFrameRelation')))
                g.add((matchedFrames_uri, RDFS.label, Literal(matchedFrameName)))

                g.add((frame_uri, URIRef('http://example.com/hasMatchedFrames'), matchedFrames_uri))
                g.add((matchedFrames_uri, URIRef('http://example.com/relatesTo'), frame_uri))


            # Add the triples to the graph for all tweets
            g_all_tweets += g


            # Serialize the RDF graph and save it to a file
            with open("15thMayVersion2.ttl", 'wb') as f:
                f.write(g_all_tweets.serialize(format="turtle").encode())

            print(f"RDF graph saved to 15thMayVersion2.ttl file.")


