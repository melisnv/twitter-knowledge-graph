from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file

# Competency Question:
# How can the utilization of Polarity Analysis assist in the recognition of semantic frames
# within Twitter debates, based on the information available in the knowledge graph?
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?tweetID ?frameType ?polarityValue ?tweetText
    WHERE {
        ?tweet a ns1:Tweet ;
            rdfs:label ?tweetID ;
            ns1:hasContent ?content ;
            ns1:hasInstantiatedFrame ?frame ;
            ns1:hasPolarityScore ?polarity .
        ?content rdfs:label ?tweetText .
        ?polarity rdfs:label ?polarityValue .
        ?frame ns1:hasFrameType ?frameType .
        FILTER (CONTAINS(lcase(?tweetText), "black") && CONTAINS(lcase(?tweetText), "income") && xsd:decimal(?polarityValue) < 0.0)
    }
    ORDER BY DESC(xsd:decimal(?polarityValue))
"""

# executing the combined query and get the results
results = graph.query(query)  # Updated namespace prefix

# iterating through the query results
for row in results:
    tweetID = row['tweetID']
    tweetText = row['tweetText']
    frameType = row['frameType'].split("/")[-1]
    polarityValue = row['polarityValue']

    print(f"tweetID:{tweetID} frame : {frameType} polarity:{polarityValue} tweetText:{tweetText}")
    print("---------------------------")