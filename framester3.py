import requests
import json
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

headers = {
    'Content-Type': 'application/json',
}

fcg_url = "http://127.0.0.1:1170/extract-frames"

data = {
    "utterance": "A court in Russia sentences ex journalist IvanSafronov to 22 years in a penal colony after finding him guilty of treason, in a landmark case for the Kremlin’s crackdown on press freedom.",
    #"utterance": "This work combines economic and demographic data to examine inequality of living standards in Stockholm at the turn of the twentieth century.",
    "package": "propbank-grammar",
    "grammar": "*propbank-grammar*",
    "timeout": 100,
}

# Send a request to the Frame Extractor API to extract frames from the input utterance
response = requests.post(fcg_url, headers=headers, json=data)
fcg_output = json.loads(response.text)

# Iterate over the extracted frames and query Framester for additional information about each frame
for frame in fcg_output["frameSet"]:
    frame_name = frame["frameName"]
    #frame_type = frame_name.split(".")[0]
    print(frame_name)

    # Construct the SPARQL query to retrieve information about the frame from Framester
    sparql_template2 = r'''
    PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
    SELECT DISTINCT ?frame ?related ?closeFrames 
    WHERE {{
    ?frame a tbox:Frame ;
        tbox:hasFrameRelation ?related ;
        skos:closeMatch ?closeFrames .
    FILTER regex(str(?closeFrames), "{frame_name}")
    }}
    '''

    sparql_query = sparql_template2.format(frame_name=frame_name, sent_number=1)

    # Send the SPARQL query to the Framester endpoint and retrieve the results
    framester_endpoint_url = "http://etna.istc.cnr.it/framester2/sparql"
    framester_response = requests


    # set the request headers and data
    data = {'query': sparql_query}

    sparql = SPARQLWrapper("http://etna.istc.cnr.it/framester2/sparql")
    sparql.setQuery(sparql_query)
    sparql.method = 'GET'
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    print(json.dumps(results, indent=4))
