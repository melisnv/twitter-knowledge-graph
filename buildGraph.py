import rdflib
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS
import json

# Read the merged JSON data
with open('data/combined.json') as file:
    merged_data = json.load(file)

# Define RDF namespaces
fv = Namespace('https://w3id.org/framester/ontology/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

# Create an RDF graph
g_all_tweets = Graph()

# Iterate over merged data
for entry in merged_data:
    frame_name = entry['frame_name']
    tweet_id = entry['tweet_id']
    topics = entry['topics']
    results = entry['results']

    # Create tweet URI
    tweet_uri = rdflib.URIRef(tweet_id)

    # Add tweet triples
    g_all_tweets.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
    g_all_tweets.add((tweet_uri, RDFS.label, Literal(tweet_id)))

    # Add topic triples
    for topic in topics:
        topic_uri = rdflib.URIRef(topic)
        g_all_tweets.add((topic_uri, RDF.type, URIRef('http://example.com/Topic')))
        g_all_tweets.add((topic_uri, RDFS.label, Literal(topic_uri)))
        g_all_tweets.add((topic_uri, URIRef('http://example.com/isAbout'), tweet_uri))

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

        g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasFrame'), frame_uri))
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
with open("graphs/21thMay.ttl", 'wb') as f:
    f.write(g_all_tweets.serialize(format="turtle").encode())

print(f"RDF graph saved to 21thMay.ttl file.")