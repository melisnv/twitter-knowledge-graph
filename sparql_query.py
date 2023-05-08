import requests
import urllib.parse

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX frdf: <http://framester.risis.eu/v1/frdf/ontology/framester-schema#>
SELECT * WHERE {
    ?sub ?pred ?obj
}
"""

framester_endpoint = 'http://etna.istc.cnr.it/framester2/sparql'

response = requests.get(framester_endpoint, data={'query': query})

# params = {'query': urllib.parse.quote(query)}
# response = requests.get(framester_endpoint, params=params)

if response.status_code == 200:
    #print(response.content)
    content = response.content
    print(content)
    # process the data as needed
else:
    print("Error: ", response.status_code, response.text)
    print(f"Error: {response.status_code}")