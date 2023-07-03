from rdflib import Graph, Namespace
import pandas as pd
from collections import defaultdict

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows
pd.set_option('display.width', None)        # Auto-adjust width

# loading the knowledge graph from the TTL file
g = Graph()
g.parse("graphs/1stJuly2.ttl", format="ttl")

# defining the namespaces used in the TTL file
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# discovering topics and their related frames
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?tweetID ?relatedTopic
    WHERE {
      ?topic a <http://example.com/Topic/> ;
             ns1:topicOf ?tweetID ;
             rdfs:label ?label .
      
      ?relatedTopic a <http://example.com/Topic/> ;
                    ns1:topicOf ?topicOf ;
                    rdfs:label ?relatedLabel .
      
      FILTER(?topic != ?relatedTopic)
      
      BIND(REPLACE(STR(?tweetID), "http://example.org/FrameNumber/", "") AS ?tweetIDFrame)
      BIND(REPLACE(STR(?topicOf), "http://example.org/FrameNumber/", "") AS ?topicOfFrame)
      
      FILTER(?tweetIDFrame = ?topicOfFrame)
    }
    """

# executing the query and retrieve the results
results = g.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

# a dictionary to store the tweet ID and related topics as set
result_dict = defaultdict(set)

for result in results:
    tweetID = result[0].split("/")[-2]
    relatedTopic = result[1].split("/")[-1]
    result_dict[tweetID].add(relatedTopic)

# print the grouped results
for tweetID, relatedTopics in result_dict.items():
    print(f"Tweet ID: {tweetID}")
    print("Related Topics:", ", ".join(relatedTopics))
    print()

