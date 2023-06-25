from rdflib import Graph, Namespace
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows
pd.set_option('display.width', None)        # Auto-adjust width

# loading the knowledge graph from the TTL file
g = Graph()
g.parse("graphs/15thJune3.ttl", format="ttl")

# defining the namespaces used in the TTL file
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# defining the SPARQL query
# discovering topics and their related frames
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?topic ?frame
    WHERE {
      ?topic a <http://example.com/Topic/> ;
             ns1:topicOf ?frame .
    }
    """

# executing the query and retrieve the results
results = g.query(query, initNs={"ns1": ns1, "rdfs": rdfs})
print(results)

# a list to store the query results
query_results = []

for row in results:
    frame = str(row["frame"])
    topic = str(row["topic"])
    query_results.append({"Frame": frame, "topic": topic})

df = pd.DataFrame(query_results)
df_str = df.to_string(max_colwidth=100)


print(df_str)

