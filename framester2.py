import rdflib
import requests
import json
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal, OWL
from rdflib.namespace import RDF, RDFS, XSD
#from rdflib_hdt import HDTStore, optimize_sparql

headers = {
    'Content-Type': 'application/json',
}

fcg_url = "http://127.0.0.1:1170/extract-frames"

data = {
    #"utterance": "A court in Russia sentences ex journalist IvanSafronov to 22 years in a penal colony after finding him guilty of treason, in a landmark case for the Kremlin’s crackdown on press freedom.",
    "utterance": "This work combines economic and demographic data to examine inequality of living standards in Stockholm at the turn of the twentieth century.",
    "package": "propbank-grammar",
    "grammar": "*propbank-grammar*",
    "timeout": 100,
}

# a request to the Frame Extractor API to extract frames from the input utterance
response = requests.post(fcg_url, headers=headers, json=data)
fcg_output = json.loads(response.text)
print(fcg_output)
print("\n")

# an RDF graph
g = Graph()

# defining namespaces for Framester and WebVOWL
fv = Namespace('https://w3id.org/framester/ontology/')
vowl = Namespace('http://www.w3.org/2002/07/owl#')
FRAME = Namespace('https://w3id.org/framester/framenet/tbox/')

# iterating over the extracted frames and query Framester for additional information about each frame
for frame in fcg_output["frameSet"]:
    frame_name = frame["frameName"]
    print(frame_name)

    # the SPARQL query to retrieve information about the frame from Framester
    sparql_template = r'''
    PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
    SELECT DISTINCT ?frame ?name ?def ?matchedFrames ?closeFrames 
    WHERE {{
    ?frame a tbox:Frame ;
        tbox:frame_name ?name ;
        rdfs:comment ?def ;
        skos:closeMatch ?matchedFrames ;
        skos:closeMatch ?closeFrames .
    FILTER regex(str(?closeFrames), "{frame_name}")
    }}
    '''

    #sparql_template = r'''
    #    PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
    #    SELECT DISTINCT ?frame ?name ?def ?matchedFrames ?hasFrameElement ?closeFrames
    #    WHERE {{
    #    ?frame a tbox:Frame ;
    #        tbox:frame_name ?name ;
    #        rdfs:comment ?def ;
    #        tbox:hasFrameElement ?hasFrameElement ;
    #        skos:closeMatch ?matchedFrames ;
    #        skos:closeMatch ?closeFrames .
    #    FILTER regex(str(?closeFrames), "{frame_name}")
    #    }}
    #    '''

    sparql_query = sparql_template.format(frame_name=frame_name, sent_number=1)
    sparql = SPARQLWrapper("http://etna.istc.cnr.it/framester2/sparql")
    sparql.setTimeout(300)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print("RESULTS:", results)

    # looping through the SPARQL query results and add triples for each URL
    for result in results['results']['bindings']:
        # creating RDFLib URIRef for the frame URI
        frame_uri = rdflib.URIRef(result['frame']['value'])
        frame = rdflib.URIRef(result['frame']['value']).split("/")[-1]
        #hasFrame_uri = rdflib.URIRef(result['hasFrameElement']['value'])
        #hasFrame =  result['hasFrameElement']['value'].split("/")[-1]

        matchedFrames_uri = rdflib.URIRef(result['matchedFrames']['value'])
        matchedFrames = result['matchedFrames']['value'].split("/")[-1]

        # definition
        sentences = result['def']['value'].split('.')
        definition = sentences[0].strip()

        g.add((frame_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/tbox/Frame')))
        g.add((frame_uri, RDFS.label, Literal(result['name']['value'])))
        g.add((frame_uri, RDFS.comment, Literal(definition)))
        #g.add((frame_uri, RDFS.domain, Literal(hasFrame)))

        #g.add((hasFrame, RDF.type, hasFrame_uri))
        #g.add((hasFrame_uri, RDF.type, URIRef('https://w3id.org/framester/framenet/tbox/hasFrameElement')))
        #g.add((hasFrame_uri, RDFS.label, Literal(hasFrame)))
        #g.add((hasFrame_uri, RDFS.range, frame_uri))

        g.add((matchedFrames_uri, RDF.type, matchedFrames_uri))
        g.add((matchedFrames_uri, RDFS.label, Literal(matchedFrames)))
        g.add((matchedFrames_uri, RDFS.range, frame_uri))

    # serializing the RDF graph in Turtle format
    print("***********")
    print(g.serialize(format='turtle'))

    # saving the output as RDF file
    with open('newAttempt.ttl', 'wb') as f:
        f.write(g.serialize(format="turtle").encode())

    print("RDF graph saved to newAttempt.ttl file.")