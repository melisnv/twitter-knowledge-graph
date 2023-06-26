from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/26thJunedeneme.ttl", format="ttl")

# defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# querying for tweets with the highest polarity score
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?tweet ?polarityValue ?tweetText WHERE {
      ?polarity a ns1:Polarity ;
                rdfs:label ?polarityValue .
      ?tweet a ns1:Content ;
             rdfs:label ?tweetID ;
             rdfs:label ?tweetText .
      FILTER NOT EXISTS {
        ?otherPolarity a ns1:Polarity ;
                       rdfs:label ?otherPolarityValue .
        FILTER (?otherPolarityValue > ?polarityValue)
      }
    }
    """

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

# the query results
for result in results:
    tweet_id = result[0].split("/")[-1]  # Extract the value after the last '/'
    polarity_value = result[1].split("/")[-1]  # Extract the value after the last '/'
    tweet_text = result[2]
    print(f"Tweet ID: {tweet_id}, Polarity: {polarity_value}, Text: {tweet_text}")
