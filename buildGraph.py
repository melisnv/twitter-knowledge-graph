import re
import urllib

import rdflib
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS
import json

# Read the merged JSON data
with open('data/combined.json') as file:
    merged_data = json.load(file)

# Define RDF namespaces
fv = Namespace('https://w3id.org/framester/ontology/')
framespace = Namespace('https://example.org/')
twt = Namespace('https://example.org/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

# Create an RDF graph
g_all_tweets = Graph()

# Iterate over merged data
for entry in merged_data:
    frame_name = entry['frame_name']
    tweet_id = entry['tweet_id']
    frame_roles = entry['frame_roles']
    topics = entry['topics']
    results = entry['results']

    # creating tweet URI and frameURI
    frame_FCG = framespace[frame_name]
    tweet_uri = twt[tweet_id]
    #tweet_uri = rdflib.URIRef(tweet_id)

    print(frame_FCG)
    print(tweet_uri)

    # creating intermediate node URI
    intermediate_node_uri = fv['intermediateNode']

    # adding tweet triples and frame triple
    g_all_tweets.add((intermediate_node_uri, RDF.type, URIRef('http://example.com/IntermediateNode')))
    g_all_tweets.add((intermediate_node_uri, URIRef('http://example.com/connects'), tweet_uri))
    g_all_tweets.add((intermediate_node_uri, URIRef('http://example.com/connects'), frame_FCG))

    g_all_tweets.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
    g_all_tweets.add((tweet_uri, RDFS.label, Literal(tweet_id)))

    g_all_tweets.add((frame_FCG, RDF.type, URIRef('http://example.com/Frame')))
    g_all_tweets.add((frame_FCG, RDFS.label, Literal(frame_name)))
    g_all_tweets.add((frame_FCG, URIRef('http://example.com/frameOf'), intermediate_node_uri))
    g_all_tweets.add((intermediate_node_uri, URIRef('http://example.com/hasFrame'), frame_FCG))


    # adding frame roles
    for role,value_list in frame_roles.items():
        for value in value_list: # extra loop inside of value_list
            print(value)

            modified_value = value.replace(" ", "-")
            modified_value = re.sub("[']", "", modified_value)
            role_string = rdflib.URIRef(f'http://example.com/{modified_value}')
            role_arg = rdflib.URIRef(role)
            role_capitalize = role.capitalize()

            g_all_tweets.add((intermediate_node_uri, URIRef(f'http://example.com/hasArgument'), role_arg))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/{role}Of'), intermediate_node_uri))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/hasValue'), role_string))


    # adding topic triples
    for topic in topics:
        topic_uri = rdflib.URIRef(topic)
        g_all_tweets.add((topic_uri, RDF.type, URIRef('http://example.com/Topic')))
        g_all_tweets.add((topic_uri, RDFS.label, Literal(topic_uri)))
        g_all_tweets.add((intermediate_node_uri, URIRef('http://example.com/isAbout'), topic_uri))
        g_all_tweets.add((topic_uri, URIRef('http://example.com/topicOf'), intermediate_node_uri))

    # processing frame-related results
    hasFrame_results = results['hasFrame']
    closeMatch_results = results['closeMatch']

    for result in hasFrame_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]  # Extract the frame name from the URL

        relatedFrame_uri = rdflib.URIRef(result['related']['value'])
        relatedFrameName = result['related']['value'].split("/")[-1]  # Extract the frame name from the URL

        # adding frame triples
        g_all_tweets.add((frame_uri, RDF.type, URIRef('http://example.com/Frame')))
        g_all_tweets.add((frame_uri, RDFS.label, Literal(frameName)))

        # adding hasFrameRelation
        g_all_tweets.add((relatedFrame_uri, RDF.type, URIRef('http://example.com/SymmetricProperty')))
        g_all_tweets.add((relatedFrame_uri, RDFS.label, Literal(relatedFrameName)))

        g_all_tweets.add((frame_FCG, URIRef('http://example.com/closeMatchOf'), frame_uri))
        g_all_tweets.add((frame_uri, URIRef('http://example.com/hasFrameRelation'), relatedFrame_uri))
        g_all_tweets.add((relatedFrame_uri, URIRef('http://example.com/isRelated'), frame_uri))

    for result in closeMatch_results:
        matchedFrames_uri = rdflib.URIRef(result['matchedFrames']['value'])
        matchedFrameName = result['label']['value'].split("/")[-1]

        # adding closeMatch frames
        g_all_tweets.add((matchedFrames_uri, RDF.type, URIRef('http://example.com/NounSynset')))
        g_all_tweets.add((matchedFrames_uri, RDFS.label, Literal(matchedFrameName)))

        g_all_tweets.add((frame_uri, URIRef('http://example.com/closeMatchFrame'), matchedFrames_uri))
        g_all_tweets.add((matchedFrames_uri, URIRef('http://example.com/synonymOf'), frame_uri))

# Serialize the RDF graph and save it to a file
with open("graphs/letsnottrythis.ttl", 'wb') as f:
    f.write(g_all_tweets.serialize(format="turtle").encode())

print(f"RDF graph saved to letsnottrythis.ttl file.")