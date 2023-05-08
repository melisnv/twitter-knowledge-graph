import requests
import json
from SPARQLWrapper import SPARQLWrapper, JSON

headers = {
    'Content-Type': 'application/json',
}

# Set up the input data for the Frame Extractor API
data = {
    "utterance": "This work combines economic and demographic data to examine inequality of living standards in Stockholm at the turn of the twentieth century.",
    "package": "propbank-grammar",
    "grammar": "*propbank-grammar*",
    "timeout": 100,
}

# Send a request to the Frame Extractor API to extract frames from the input utterance
fcg_url = "http://127.0.0.1:1170/extract-frames"
response = requests.post(fcg_url, headers=headers, json=data)
fcg_output = json.loads(response.text)
print("FCG OUTPUT: ",fcg_output)

# Iterate over the extracted frames and query Framester for additional information about each frame
frames = []
for frame in fcg_output["frameSet"]:
    frame_name = frame["frameName"]
    frame_type = frame_name.split(".")[0]

    # Construct the SPARQL query to retrieve information about the frame from Framester
    sparql_template = '''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT * WHERE {{
            <http://etna.istc.cnr.it/framester2/resource/{frame_name}> ?pred ?obj .
        }} LIMIT 10
    '''
    sparql_query = sparql_template.format(frame_name=frame_name)

    # Send the SPARQL query to the Framester endpoint and retrieve the results
    framester_endpoint_url = "http://etna.istc.cnr.it/framester2/sparql"
    data = {'query': sparql_query}
    response = requests.post(framester_endpoint_url, headers=headers, data=data)
    framester_output = json.loads(response.text)

    # Add the frame and its Framester information to the frames list
    frames.append({"frame": frame, "framester": framester_output})

# Send the frames list to the FrameGrapher API
fg_url = "http://127.0.0.1:8000/framegrapher/api/process_text"
data = {
    "text": data["utterance"],
    "frames": frames
}
response = requests.post(fg_url, headers=headers, json=data)
fg_output = json.loads(response.text)
print("FG OUTPUT: ", fg_output)