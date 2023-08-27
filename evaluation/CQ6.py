from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file

# Competency question:
# How can the knowledge extracted from semantic frames in Twitter data contribute to
# linguistic research and understanding language meaning in social media contexts?
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns6: <https://w3id.org/framester/framenet/tbox/> 

    SELECT ?frame ?label ?description
    WHERE {
      ?frame a <https://w3id.org/framester/framenet/abox/frame/> ;
             rdfs:label ?label ;
             rdfs:comment ?description .
    }
    """

results = graph.query(query)

# the query results
for result in results:
    frame = result[0]
    label = result[1]
    description = result[2]
    print(f"Frame: {frame},\n"
          f"Description: {description}, \n"
          f"--------------------------")
