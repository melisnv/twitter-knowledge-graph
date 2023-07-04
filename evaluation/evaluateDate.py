from tabulate import tabulate
from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/1stJuly2.ttl", format="ttl")

# Defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Construct the query with the frame URI variable
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?tweet ?createdAt
    WHERE {
      ?tweet a ns1:Tweet ;
             rdfs:label ?tweetLabel ;
             ns1:createdAt ?createdAt .
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results) == 0:
    print("The given frame is not found among the tweets.")
else:
    table = []
    for result in results:
        tweet = result[0]
        createdAt = result[1]
        table.append([tweet, createdAt])

    headers = ["Label", "Frame Relation"]
    print(tabulate(table, headers=headers))
