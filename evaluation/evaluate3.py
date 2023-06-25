from rdflib import Graph, Namespace

# Load the knowledge graph from the file
graph = Graph()
graph.parse("graphs/15thJune3.ttl", format="ttl")

# Define the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Perform a relationship-based query

# discovering tweets connecting the concepts "love" and "libs"
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?tweet
    WHERE {
        ?tweet ns1:hasFrameNumber ?frameNumber .
        ?frameNumber ns1:isAbout ?topic .
        ?topic rdfs:label "love" .
        ?topic2 rdfs:label "libs" .
        ?frameNumber ns1:isAbout ?topic2 .
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

# Print the query results
for result in results:
    print(result)
