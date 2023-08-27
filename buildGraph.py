import re
import rdflib
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS
import json

# read the merged JSON data from FCG Editor outputs and Framester outputs
with open('data/combined_outputs.json') as file:
    merged_data = json.load(file)

# defining RDF namespaces
fv = Namespace('https://w3id.org/framester/ontology/')
framespace = Namespace('https://example.org/')
topicspace = Namespace('https://example.org/Topic/')
twtcontent = Namespace('https://example.org/Content/')
core = Namespace('http://www.w3.org/2004/02/skos/core#')

# creating an RDF graph
g_all_tweets = Graph()
# initializing a counter for assigning a value to each frame
frame_counter = 1

# iterating over merged data
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
    tweet_uri = framespace[tweet_id]
    tweet_date = framespace[date]
    tweet_text = twtcontent[tweet_id] # to have unique
    tweet_subjectivity = framespace[subjectivity]
    tweet_polarity = framespace[polarity]
    tweet_analysis = framespace[analysis]


    # adding tweet triples and frame triple
    g_all_tweets.add((tweet_uri, RDF.type, URIRef('http://example.com/Tweet')))
    g_all_tweets.add((tweet_uri, RDFS.label, Literal(tweet_id)))
    # adding tweet date
    g_all_tweets.add((tweet_date, RDF.type, URIRef('http://example.com/Date')))
    g_all_tweets.add((tweet_date, RDFS.label, Literal(date)))
    g_all_tweets.add((tweet_uri, URIRef('http://purl.org/dc/terms/created'), tweet_date))
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
    g_all_tweets.add((frame_FCG, RDF.type, URIRef('https://w3id.org/framester/framenet/tbox/Frame')))
    g_all_tweets.add((frame_FCG, RDFS.label, Literal(frame_name)))
    g_all_tweets.add((frame_FCG, URIRef('http://example.com/hasFrame'), frame_number_node))
    g_all_tweets.add((frame_number_node, URIRef('http://example.com/hasFrameType'), frame_FCG))

    # incrementing frame counter
    frame_counter += 1

    # adding frame roles
    for role, value_list in frame_roles.items():
        for value in value_list:
            modified_value = value.replace(" ", "-")
            modified_value = re.sub("[']", "", modified_value)
            role_string = rdflib.URIRef(f'http://example.com/{modified_value}')
            role_arg = rdflib.URIRef(role)
            role_capitalize = role.capitalize()
            g_all_tweets.add((frame_number_node, URIRef(f'http://example.com/has{role}'), role_arg))
            g_all_tweets.add((role_arg, URIRef(f'http://example.com/hasValue'), role_string))

    # adding topic triples
    for topic in topics:
        topic_uri = topicspace[topic]
        g_all_tweets.add((topic_uri, RDF.type, URIRef('http://example.com/Topic/')))
        g_all_tweets.add((topic_uri, RDFS.label, Literal(topic)))
        g_all_tweets.add((frame_number_node, URIRef('http://example.com/hasTopic'), topic_uri))

    # processing frame-related results
    hasFrameRelation_results = results['hasFrameRelation']
    closeMatch_results = results['closeMatch']
    sameAs_results = results["sameAs"]
    hasRole_results = results["hasRole"]
    inheritsFrom_results = results["inheritsFrom"]
    hasComment_results = results["hasComment"]
    hasFrameElement_results = results["hasFrameElement"]

    hasInchoative_results = results['hasInchoative']
    isCausativeOf_results = results['isCausativeOf']
    isInchoativeOf_results = results["isInchoativeOf"]
    isPerspectivizedIn_results = results["isPerspectivizedIn"]
    narrowerMatch_results = results["narrowerMatch"]
    precedes_results = results["precedes"]
    perspectiveOn_results = results["perspectiveOn"]
    seeAlso_results = results["seeAlso"]

    for result in hasFrameRelation_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        relatedFrame_uri = rdflib.URIRef(result['related']['value'])
        relatedFrameName = result['related']['value'].split("/")[-1]
        # adding frame triples
        g_all_tweets.add((frame_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/abox/frame/')))
        g_all_tweets.add((frame_uri, RDFS.label, Literal(frameName)))
        # adding hasFrameRelation
        g_all_tweets.add((relatedFrame_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/abox/frame/')))
        g_all_tweets.add((relatedFrame_uri, RDFS.label, Literal(relatedFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('https://w3id.org/framester/framenet/tbox/hasFrameRelation'), relatedFrame_uri))

    for result in hasComment_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        hasComment_uri = rdflib.URIRef(result['comment']['value'])
        hasComment = result['comment']['value']
        g_all_tweets.add((frame_FCG, RDFS.comment, Literal(hasComment)))

    for result in sameAs_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        sameAsFrame_uri = rdflib.URIRef(result['sameAs']['value'])
        sameAsFrameName = result['label']['value']
        g_all_tweets.add((sameAsFrame_uri, RDF.type, URIRef('http://www.w3.org/2004/02/skos/core#Concept')))
        g_all_tweets.add((sameAsFrame_uri, RDFS.label, Literal(sameAsFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/2002/07/owl#sameAs'), sameAsFrame_uri))

    for result in hasRole_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        role_uri = rdflib.URIRef(result['role']['value'])
        roleName = result['role']['value'].split("/")[-1]
        role_type_uri = rdflib.URIRef(result['subsumedUnder']['value'])
        roleTypeName = result['subsumedUnder']['value'].split("/")[-1]
        g_all_tweets.add((role_uri, RDF.type, URIRef('https://w3id.org/framesterpage/pb/pbschema/Role')))
        g_all_tweets.add((role_uri, RDFS.label, Literal(roleName)))
        g_all_tweets.add((role_type_uri, RDF.type, URIRef('https://w3id.org/framesterpage/pb/pbschema/RoleType')))
        g_all_tweets.add((role_type_uri, RDFS.label, Literal(roleTypeName)))
        g_all_tweets.add((frame_FCG, URIRef('https://w3id.org/framester/pb/pbschema/hasRole'), role_uri))
        g_all_tweets.add((role_uri, URIRef('https://w3id.org/framester/schema/subsumedUnder'), role_type_uri))

    for result in closeMatch_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        matchedFrames_uri = rdflib.URIRef(result['related']['value'])
        matchedFrameName = result['related']['value'].split("/")[-1]
        # adding closeMatch frames
        g_all_tweets.add((matchedFrames_uri, RDF.type, URIRef('https://w3id.org/framesterpage/wn/wn30/schema/NounSynset')))
        g_all_tweets.add((matchedFrames_uri, RDFS.label, Literal(matchedFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/2004/02/skos/core#closeMatch'), matchedFrames_uri))

    for result in hasInchoative_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        inchoative_uri = rdflib.URIRef(result['hasInchoative']['value'])
        inchoativeFrameName = result['hasInchoative']['value'].split("/")[-1]
        g_all_tweets.add((inchoative_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((inchoative_uri, RDFS.label, Literal(inchoativeFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('https://w3id.org/framesterpage/framenet/tbox/isInchoativeOf'), inchoative_uri))

    for result in isCausativeOf_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        causativeOf_uri = rdflib.URIRef(result['isCausativeOf']['value'])
        causativeOfFrameName = result['isCausativeOf']['value'].split("/")[-1]
        g_all_tweets.add((causativeOf_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((causativeOf_uri, RDFS.label, Literal(causativeOfFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/framesterpage/framenet/tbox/isCausativeOf'), causativeOf_uri))

    for result in isInchoativeOf_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        isInchoativeOf_uri = rdflib.URIRef(result['isInchoativeOf']['value'])
        isInchoativeOfFrameName = result['isInchoativeOf']['value'].split("/")[-1]
        g_all_tweets.add((isInchoativeOf_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((isInchoativeOf_uri, RDFS.label, Literal(isInchoativeOfFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/framesterpage/framenet/tbox/isInchoativeOf'), isInchoativeOf_uri))

    for result in isPerspectivizedIn_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        perspectivizedIn_uri = rdflib.URIRef(result['isPerspectivizedIn']['value'])
        perspectivizedInFrameName = result['isPerspectivizedIn']['value'].split("/")[-1]
        g_all_tweets.add((perspectivizedIn_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((perspectivizedIn_uri, RDFS.label, Literal(perspectivizedInFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/framesterpage/framenet/tbox/isPerspectivizedIn'), perspectivizedIn_uri))

    for result in narrowerMatch_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        narrowerMatch_uri = rdflib.URIRef(result['narrowerMatch']['value'])
        narrowerMatchFrameName = result['narrowerMatch']['value'].split("/")[-1]
        g_all_tweets.add((narrowerMatch_uri, RDF.type, URIRef('https://w3id.org/framesterpage/wn/wn30/schema/AdjectiveSynset')))
        g_all_tweets.add((narrowerMatch_uri, RDFS.label, Literal(narrowerMatchFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/2004/02/skos/core#narrowerMatch'), narrowerMatch_uri))

    for result in precedes_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        precedes_uri = rdflib.URIRef(result['precedes']['value'])
        precedesFrameName = result['precedes']['value'].split("/")[-1]
        g_all_tweets.add((precedes_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((precedes_uri, RDFS.label, Literal(precedesFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('https://w3id.org/framesterpage/framenet/tbox/precedes'), precedes_uri))

    for result in perspectiveOn_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        perspectiveOn_uri = rdflib.URIRef(result['perspectiveOn']['value'])
        perspectiveOnFrameName = result['perspectiveOn']['value'].split("/")[-1]
        g_all_tweets.add((perspectiveOn_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((perspectiveOn_uri, RDFS.label, Literal(perspectiveOnFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('https://w3id.org/framesterpage/framenet/tbox/perspectiveOn'), perspectiveOn_uri))

    for result in seeAlso_results:
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frameName = result['frame']['value'].split("/")[-1]
        seeAlso_uri = rdflib.URIRef(result['seeAlso']['value'])
        seeAlsoFrameName = result['seeAlso']['value'].split("/")[-1]
        g_all_tweets.add((seeAlso_uri, RDF.type, URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')))
        g_all_tweets.add((seeAlso_uri, RDFS.label, Literal(seeAlsoFrameName)))
        g_all_tweets.add((frame_FCG, URIRef('http://www.w3.org/framesterpage/framenet/tbox/seeAlso'), seeAlso_uri))

# serializing the RDF graph and saving it to a file
with open("graphs/twitterKnowledgeGraph.ttl", 'wb') as f:
    f.write(g_all_tweets.serialize(format="turtle").encode())

print(f"RDF graph saved to twitterKnowledgeGraph.ttl file.")

# incrementing the frame number for the next tweet
frame_counter += 1
