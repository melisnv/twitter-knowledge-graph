from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/1stJuly2.ttl", format="ttl")

ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?tweetID ?tweetText ?topicLabel ?polarityValue WHERE {
      ?tweet a ns1:Tweet ;
             rdfs:label ?tweetID ;
             ns1:hasContent ?content ;
             ns1:hasInstantiatedFrame ?frame ;
             ns1:hasPolarityScore ?polarity .
      ?content rdfs:label ?tweetText .
      ?frame ns1:isAbout ?topic .
      ?topic rdfs:label ?topicLabel .
      ?polarity rdfs:label ?polarityValue .
      FILTER (CONTAINS(lcase(?topicLabel), "inequality") && xsd:decimal(?polarityValue) > 0.05)
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

# query results
for result in results:
    tweet_id = result[0].split("/")[-1]  # Extract the value after the last '/'
    tweet_text = result[1]
    topic_label = result[2]
    polarity = result[3]
    print(f"Tweet ID: {tweet_id}, Polarity:{polarity} Text: {tweet_text}, Topic: {topic_label}")
