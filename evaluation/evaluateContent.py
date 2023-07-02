from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/1stJuly2.ttl", format="ttl")

# Defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# all the tweet content and their IDs
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?tweet_id ?content_label
    WHERE {
      ?tweet_id a ns1:Tweet ;
                ns1:hasContent ?content .
      ?content rdfs:label ?content_label .
    }

"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results) == 0:
    print("The given frame is not found among the tweets.")
else:
    for result in results:
        tweet_id = result[0]
        content = result[1]
        print(f"Tweet: {tweet_id} Text: {content}")

print("\n")


second_graph = Graph()
second_graph.parse("graphs/26thJunedeneme.ttl", format="ttl")

# filtering condition ensures that only the tweets with content containing the term "x" are returned
query_second = """
   PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?tweet_id ?content_label
    WHERE {
      ?tweet_id a ns1:Tweet ;
                ns1:hasContent ?content .
      ?content rdfs:label ?content_label .
      
      FILTER(CONTAINS(LCASE(?content_label), "minnesota"))
    }
"""

results_second = second_graph.query(query_second, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results_second) == 0:
    print("The given frame is not found among the tweets.")
else:
    for res in results_second:
        id_tweet = res[0]
        content_label = res[1]
        print(f"Tweet: {id_tweet} Text: {content_label}")