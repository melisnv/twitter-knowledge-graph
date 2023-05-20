import json
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from SPARQLWrapper import SPARQLWrapper, JSON

# Load the fcg_output.json file
with open('data/fcg_output.json') as f:
    fcg_output_list = json.load(f)

# Load the merged.json file
with open('data/merged.json') as f:
    merged_output_dict = json.load(f)

# an RDF graph
g = Graph()

# defining namespaces for Framester and WebVOWL
fv = Namespace('https://w3id.org/framester/ontology/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

for output, merged_output in zip(fcg_output_list, merged_output_dict['results']['bindings']):
    print("MERGED OUTPUT",merged_output)
    print("OUTPUT",output)
    print("\n")

    if output.get("frameSet") is not None and output["frameSet"] is not None:
        frame_set = output["frameSet"]
        tweet_id = output["id"]
        topic_list = output['topic'].split(', ')  # make topics list
        tweet_frames = {}

        for frame in frame_set:
            frame_name = frame["frameName"]
            roles = frame["roles"]
            frame_roles = {}

            for role in roles:
                role_name = role["role"]
                role_string = role["string"]
                frame_roles[role_name] = role_string
                print(
                    f"Tweet ID: {tweet_id}, Frame: {frame_name}, Role: {role_name}, String: {role_string}, Topic: {topic_list}")

            tweet_frames[frame_name] = frame_roles

            # Access the relevant data from merged_output
            matched_frame_name = frame_name
            print("matched frame name", matched_frame_name)


            merged_output = next((item for item in merged_output_dict['results']['bindings'] if
                                  item['frame']['value'] == matched_frame_name), None)

            print(merged_output)