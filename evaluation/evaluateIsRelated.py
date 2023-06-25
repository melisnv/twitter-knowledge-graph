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
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?frame ?label ?isRelated
    WHERE {
        ?frame a ns1:Frame ;
               rdfs:label ?label ;
               ns1:isRelated ?isRelated .
    }
"""

# executing the query and retrieve the results
results = g.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

# a list to store the query results
query_results = []

for row in results:
    frame = str(row["frame"])
    label = str(row["label"])
    is_related = str(row["isRelated"])
    query_results.append({"Frame": frame, "Label": label, "IsRelated": is_related})

df = pd.DataFrame(query_results)
df_str = df.to_string(max_colwidth=100)


print(df_str)

