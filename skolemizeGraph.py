import re
import urllib

import rdflib
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, BNode
import json

# Read the merged JSON data
with open('data/combined.json') as file:
    merged_data = json.load(file)

# Define RDF namespaces
fv = Namespace('https://w3id.org/framester/ontology/')
framespace = Namespace('https://example.org/')
topicspace = Namespace('https://example.org/Topic/')
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

    # adding tweet triples and frame triple
    g_all_tweets.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
    g_all_tweets.add((tweet_uri, RDFS.label, Literal(tweet_id)))

    g_all_tweets.add((frame_FCG, RDF.type, URIRef('http://example.com/Frame')))
    g_all_tweets.add((frame_FCG, RDFS.label, Literal(frame_name)))
    g_all_tweets.add((frame_FCG, URIRef('http://example.com/frameOf'), tweet_uri))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasFrame'), frame_FCG))


    # adding frame roles
    for role,value_list in frame_roles.items():
        for value in value_list: # extra loop inside of value_list
            print(value)

            modified_value = value.replace(" ", "-")
            modified_value = re.sub("[']", "", modified_value)
            role_string = rdflib.URIRef(f'http://example.com/{modified_value}')
            #role_string = rdflib.URIRef(value)
            role_arg = rdflib.URIRef(role)
            role_capitalize = role.capitalize()

            g_all_tweets.add((tweet_uri, URIRef(f'http://example.com/hasArgument'), role_arg))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/{role}Of'), tweet_uri))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/hasValue'), role_string))


    # adding topic triples
    for topic in topics:
        topicsNode = URIRef(f"http://example.org/Topics/{tweet_id}")
        g_all_tweets.add((topicsNode, RDFS.label, Literal("Topics")))
        g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasTopics'), topicsNode))
        g_all_tweets.add((topicsNode, URIRef('http://example.com/topicsOf'), tweet_uri))

        topic_uri = topicspace[topic]
        #topic_uri = rdflib.URIRef(topic)
        g_all_tweets.add((topic_uri, RDF.type, URIRef('http://example.com/Topic/')))
        g_all_tweets.add((topic_uri, RDFS.label, Literal(topic)))
        g_all_tweets.add((topicsNode, URIRef('http://example.com/isAbout'), topic_uri))
        g_all_tweets.add((topic_uri, URIRef('http://example.com/topicOf'), topicsNode))


# Serialize the RDF graph and save it to a file
with open("graphs/yetherSON.ttl", 'wb') as f:
    f.write(g_all_tweets.serialize(format="turtle").encode())

print(f"RDF graph saved to yetherSON.ttl file.")