from rdflib import Graph, Namespace
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', None)  # Auto-adjust width

# loading the knowledge graph from the TTL file
g = Graph()
g.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file

# Competency Question:
# How does frame semantics relate linguistic utterances to word knowledge, such as event types and roles?
query = """
    PREFIX ns2: <https://w3id.org/framester/framenet/tbox/>
    PREFIX ns3: <https://w3id.org/framester/pb/pbschema/>
    PREFIX ns8: <https://w3id.org/framester/schema/>
    
    SELECT ?frame ?role ?subsumedUnder
    WHERE {
      ?frame a ns2:Frame ;
             ns3:hasRole ?role .
      
      ?role ns8:subsumedUnder ?subsumedUnder .
    }

"""

# executing the query and retrieve the results
results = g.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

query_results = []

for row in results:
    role = str(row["role"]).split("/")[-1]
    frame = str(row["frame"]).split("/")[-1]
    subsumedUnder = str(row["subsumedUnder"]).split("/")[-1]
    query_results.append({ "Frame": frame, "The Role": role, "Role Type": subsumedUnder})

df = pd.DataFrame(query_results)
df_str = df.to_string(max_colwidth=100)

print(df_str)

