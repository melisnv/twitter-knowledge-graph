from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file

# Competency Questions:
# 1) Drawing from the knowledge graph, how does the investigation of Twitter debates through the lens of
# semantic frames contribute to the existing body of literature concerning public attitudes towards
# "immigration", "climate" change, and public "health"?

# 2) How does the examination of Twitter debates, enriched by incorporating the associated frames
# of semantic frames, enhance the current body of literature on the public's perception of a particular topic?

query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns5: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?tweetID ?frameType ?tweetText ?closeMatch
    WHERE {
        ?tweet a ns1:Tweet ;
            rdfs:label ?tweetID ;
            ns1:hasContent ?content ;
            ns1:hasInstantiatedFrame ?frame .
        ?content rdfs:label ?tweetText .
        ?frame ns1:hasFrameType ?frameType .

        OPTIONAL {
            ?frameType ns5:closeMatch ?closeMatch .
        }

        FILTER (CONTAINS(lcase(?tweetText), "health"))
    }
"""

results = graph.query(query)

# processing the query results programmatically to achieve the desired grouping and concatenation effect
grouped_results = {}
for row in results:
    tweetID = row['tweetID']
    tweetText = row['tweetText']
    frameType = row['frameType'].split("/")[-1]
    closeMatch = row.get('closeMatch', '')

    if closeMatch is not None:
        closeMatch = closeMatch.split("/")[-1]

    if tweetID not in grouped_results:
        grouped_results[tweetID] = {'tweetText': tweetText, 'frames': {}}

    if frameType not in grouped_results[tweetID]['frames']:
        grouped_results[tweetID]['frames'][frameType] = []

    if closeMatch:
        grouped_results[tweetID]['frames'][frameType].append(closeMatch)

# printing the processed results
for tweetID, data in grouped_results.items():
    tweetText = data['tweetText']
    frame_info = data['frames']

    print(f"tweetID:{tweetID} \n tweetText:{tweetText}")
    for frameType, closeMatches in frame_info.items():
        closeMatches_str = ", ".join(closeMatches)
        print(f"frameType: {frameType} closeMatches: {closeMatches_str}")
    print("---------------------------")
