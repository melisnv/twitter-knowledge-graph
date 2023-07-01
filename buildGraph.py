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
topicspace = Namespace('https://example.org/Topic/')
twt = Namespace('https://example.org/')
twtcontent = Namespace('https://example.org/Content/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

# Create an RDF graph
g_all_tweets = Graph()

# Initialize frame counter
frame_counter = 1

# Iterate over merged data
for entry in merged_data:
    frame_name = entry['frame_name']
    tweet_id = entry['tweet_id']
    frame_roles = entry['frame_roles']
    topics = entry['topics']
    results = entry['results']
    date = entry['date']
    text = entry['text']
    subjectivity = entry['subjectivity']
    polarity = entry['polarity']
    analysis = entry['analysis']

    # creating tweet URI and frameURI
    frame_FCG = framespace[frame_name]
    tweet_uri = twt[tweet_id]
    tweet_date = twt[date]
    tweet_text = twtcontent[tweet_id] # to have unique
    tweet_subjectivity = twt[subjectivity]
    tweet_polarity = twt[polarity]
    tweet_analysis = twt[analysis]

    # adding tweet triples and frame triple
    g_all_tweets.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
    g_all_tweets.add((tweet_uri, RDFS.label, Literal(tweet_id)))

    # adding tweet date
    g_all_tweets.add((tweet_date, RDF.type, URIRef('http://example.com/Date')))
    g_all_tweets.add((tweet_date, RDFS.label, Literal(date)))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/createdAt'), tweet_date))

    # adding tweet text
    g_all_tweets.add((tweet_text, RDF.type, URIRef('http://example.com/Content')))
    g_all_tweets.add((tweet_text, RDFS.label, Literal(text)))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasContent'), tweet_text))

    # adding tweet subjectivity
    g_all_tweets.add((tweet_subjectivity, RDF.type, URIRef('http://example.com/Subjectivity')))
    g_all_tweets.add((tweet_subjectivity, RDFS.label, Literal(subjectivity)))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasSubjectivityScore'), tweet_subjectivity))

    # adding tweet subjectivity
    g_all_tweets.add((tweet_polarity, RDF.type, URIRef('http://example.com/Polarity')))
    g_all_tweets.add((tweet_polarity, RDFS.label, Literal(polarity)))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasPolarityScore'), tweet_polarity))

    # adding tweet analysis
    g_all_tweets.add((tweet_analysis, RDF.type, URIRef('http://example.com/Analysis')))
    g_all_tweets.add((tweet_analysis, RDFS.label, Literal(analysis)))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasAnalysis'), tweet_analysis))

    # adding frame number
    frame_number_node = URIRef(f"http://example.org/FrameNumber/{tweet_id}/{frame_counter}")
    g_all_tweets.add((frame_number_node, RDFS.label, Literal(str(frame_counter))))
    g_all_tweets.add((tweet_uri, URIRef('http://example.com/hasInstantiatedFrame'), frame_number_node))
    #g_all_tweets.add((frame_number_node, URIRef('http://example.com/instantiatedFrameOf'), tweet_uri))

    g_all_tweets.add((frame_FCG, RDF.type, URIRef('http://example.com/Frame')))
    g_all_tweets.add((frame_FCG, RDFS.label, Literal(frame_name)))
    g_all_tweets.add((frame_FCG, URIRef('http://example.com/frameOf'), frame_number_node))
    g_all_tweets.add((frame_number_node, URIRef('http://example.com/hasFrameType'), frame_FCG))

    # incrementing frame counter
    frame_counter += 1

    # adding frame roles
    for role, value_list in frame_roles.items():
        for value in value_list:
            print(value)

            modified_value = value.replace(" ", "-")
            modified_value = re.sub("[']", "", modified_value)
            role_string = rdflib.URIRef(f'http://example.com/{modified_value}')
            role_arg = rdflib.URIRef(role)
            role_capitalize = role.capitalize()

            g_all_tweets.add((frame_number_node, URIRef(f'http://example.com/has{role}'), role_arg))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/{role}Of'), frame_number_node))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/hasValue'), role_string))

    # adding topic triples
    for topic in topics:
        topic_uri = topicspace[topic]
        g_all_tweets.add((topic_uri, RDF.type, URIRef('http://example.com/Topic/')))
        g_all_tweets.add((topic_uri, RDFS.label, Literal(topic)))
        g_all_tweets.add((frame_number_node, URIRef('http://example.com/isAbout'), topic_uri))
        g_all_tweets.add((topic_uri, URIRef('http://example.com/topicOf'), frame_number_node))

    # processing frame-related results
    hasFrameRelation_results = results['hasFrameRelation']
    closeMatch_results = results['closeMatch']
    sameAs_results = results["sameAs"]
    hasRole_results = results["hasRole"]
    inheritsFrom_results = results["inheritsFrom"]
    hasComment_results = results["hasComment"]
    hasFrameElement_results = results["hasFrameElement"]

    for result in hasComment_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]

        hasComment_uri = rdflib.URIRef(result['comment']['value'])
        hasComment = result['comment']['value']

        g_all_tweets.add((frame_FCG, RDFS.comment, Literal(hasComment)))


    for result in hasFrameRelation_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]

        relatedFrame_uri = rdflib.URIRef(result['related']['value'])
        relatedFrameName = result['related']['value'].split("/")[-1]

        # adding frame triples
        g_all_tweets.add((frame_uri, RDF.type, URIRef('http://example.com/Frame')))
        g_all_tweets.add((frame_uri, RDFS.label, Literal(frameName)))

        # adding hasFrameRelation
        g_all_tweets.add((relatedFrame_uri, RDF.type, URIRef('http://example.com/SymmetricProperty')))
        g_all_tweets.add((relatedFrame_uri, RDFS.label, Literal(relatedFrameName)))

        g_all_tweets.add((frame_FCG, URIRef('http://example.com/closeMatchOf'), frame_uri))
        g_all_tweets.add((frame_uri, URIRef('http://example.com/hasFrameRelation'), relatedFrame_uri))
        g_all_tweets.add((relatedFrame_uri, URIRef('http://example.com/isRelated'), frame_uri))

    for result in sameAs_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]

        sameAsFrame_uri = rdflib.URIRef(result['sameAs']['value'])
        sameAsFrameName = result['label']['value']

        # adding sameAs
        g_all_tweets.add((sameAsFrame_uri, RDF.type, URIRef('http://example.com/EquivalentClass')))
        g_all_tweets.add((sameAsFrame_uri, RDFS.label, Literal(sameAsFrameName)))

        g_all_tweets.add((frame_uri, URIRef('http://example.com/sameAs'), sameAsFrame_uri))
        g_all_tweets.add((sameAsFrame_uri, URIRef('http://example.com/similarConceptOf'), frame_uri))

    for result in hasRole_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]

        role_uri = rdflib.URIRef(result['role']['value'])
        roleName = result['role']['value'].split("/")[-1]

        hasRole_uri = rdflib.URIRef(result['subsumedUnder']['value'])
        hasRoleName = result['subsumedUnder']['value'].split("/")[-1]

        g_all_tweets.add((role_uri, RDF.type, URIRef('https://w3id.org/framester/pb/pbschema/RoleSet')))
        g_all_tweets.add((role_uri, RDFS.label, Literal(roleName)))

        g_all_tweets.add((hasRole_uri, RDF.type, URIRef('https://w3id.org/framester/pb/pbschema/Role')))
        g_all_tweets.add((hasRole_uri, RDFS.label, Literal(hasRoleName)))

        g_all_tweets.add((frame_FCG, URIRef('http://example.com/hasRoleSet'), role_uri))
        g_all_tweets.add((role_uri, URIRef('http://example.com/roleOf'), frame_FCG))

        g_all_tweets.add((role_uri, URIRef('http://example.com/subsumedUnder'), hasRole_uri))
        g_all_tweets.add((hasRole_uri, URIRef('http://example.com/transitivePropertyOf'), role_uri))

    #for result in inheritsFrom_results:
    #    frame_uri = rdflib.URIRef(result['frame']['value'])
    #    frameName = result['frame']['value'].split("/")[-1]
    #
    #    inheritsFrom_uri = rdflib.URIRef(result['inheritsFromFrame']['value'])
    #    inheritsFromName = result['inheritsFromFrame']['value'].split("/")[-1]
    #
    #    # adding sameAs
    #    g_all_tweets.add((inheritsFrom_uri, RDF.type, URIRef('http://example.com/ObjectProperty')))
    #    g_all_tweets.add((inheritsFrom_uri, RDFS.label, Literal(inheritsFromName)))
    #
    #    g_all_tweets.add((frame_uri, URIRef('http://example.com/inheritsFrom'), inheritsFrom_uri))
    #    g_all_tweets.add((inheritsFrom_uri, URIRef('http://example.com/inheritedBy'), frame_uri))

    for result in closeMatch_results:
        matchedFrames_uri = rdflib.URIRef(result['matchedFrames']['value'])
        matchedFrameName = result['label']['value'].split("/")[-1]

        # adding closeMatch frames
        g_all_tweets.add((matchedFrames_uri, RDF.type, URIRef('http://example.com/NounSynset')))
        g_all_tweets.add((matchedFrames_uri, RDFS.label, Literal(matchedFrameName)))

        g_all_tweets.add((frame_uri, URIRef('http://example.com/closeMatchFrame'), matchedFrames_uri))
        g_all_tweets.add((matchedFrames_uri, URIRef('http://example.com/synonymOf'), frame_uri))

# Serialize the RDF graph and save it to a file
with open("graphs/1Julydeneme.ttl", 'wb') as f:
    f.write(g_all_tweets.serialize(format="turtle").encode())

print(f"RDF graph saved to 26thJunedeneme.ttl file.")

# Increment the frame number for the next tweet
frame_counter += 1
