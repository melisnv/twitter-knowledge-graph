from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/1stJuly2.ttl", format="ttl")

# defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

query_combined = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?tweet ?polarityScore ?label
    WHERE {
      ?tweet a ns1:Tweet ;
             rdfs:label ?tweetLabel ;
             ns1:hasPolarityScore ?polarityScore ;
             ns1:hasContent ?content .

      ?content a ns1:Content ;
               rdfs:label ?label .
    }
"""

results_combined = graph.query(query_combined, initNs={"ns1": ns1, "rdfs": rdfs})

# the query results
for result in results_combined:
    tweet_id = result[0].split("/")[-1]  # Extract the value after the last '/'
    polarity_value = result[1].split("/")[-1]  # Extract the value after the last '/'
    label = result[2]
    print(f"Tweet ID: {tweet_id}, Polarity: {polarity_value}, Tweet: {label}")
