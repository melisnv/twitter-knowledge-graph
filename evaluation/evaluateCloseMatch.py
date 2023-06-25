from rdflib import Graph, Namespace
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows
pd.set_option('display.width', None)        # Auto-adjust width

# loading the knowledge graph from the TTL file
g = Graph()
g.parse("graphs/15thJune3.ttl", format="ttl")

# the namespaces used in the TTL file
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# the SPARQL query

# retrieving frames that are close matches of a specific frame
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?frame ?closeMatch
    WHERE {
        ?frame a ns1:Frame ;
               ns1:closeMatchOf ?closeMatch .
    }
"""

# executing the query and retrieve the results
results = g.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

query_results = []

for row in results:
    frame = str(row["frame"])
    closeMatch = str(row["closeMatch"])
    query_results.append({"Frame": frame, "closeMatch": closeMatch})

df = pd.DataFrame(query_results)
df_str = df.to_string(max_colwidth=100)

print(df_str)

