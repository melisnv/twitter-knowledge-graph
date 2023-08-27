from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file


# Competency Question:
# What are the most prevalent semantic frames employed in Twitter debates addressing topics of
# immigration, climate change, and public health, as documented in the knowledge graph?
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns5: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?frameType (COUNT(?frameType) AS ?frameCount) ?tweetText ?tweetID ?polarityValue
    WHERE {
        ?tweet a ns1:Tweet ;
            rdfs:label ?tweetID ;
            ns1:hasContent ?content ;
            ns1:hasPolarityScore ?polarity ;
            ns1:hasInstantiatedFrame ?frame .
        ?content rdfs:label ?tweetText .
        ?polarity rdfs:label ?polarityValue .
        ?frame ns1:hasFrameType ?frameType .
        FILTER (CONTAINS(lcase(?tweetText), "inequality") && xsd:decimal(?polarityValue) > 0.0)
    }
    GROUP BY ?frameType
    ORDER BY DESC(?frameCount)


"""

# the combined query and get the results
results = graph.query(query)

# iterating through the query results
for row in results:
    frameType = row['frameType'].split("/")[-1]
    frameCount = row['frameCount']
    tweetID = row['tweetID']
    tweetText = row['tweetText']
    polarityValue = row['polarityValue']

    print(f"Frame :{frameType} \n"
          f"Count : {frameCount} \n"
          f"Content of tweet: {tweetText} \n"
          f"Tweet ID: {tweetID} \n"
          f"Polarity: {polarityValue}\n"
          f"---------------------------")