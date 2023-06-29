from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/26thJunedeneme.ttl", format="ttl")

# Defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Construct the query with the frame URI variable
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?role ?label ?roleOf WHERE {
      ?roleSet a <https://w3id.org/framester/pb/pbschema/RoleSet> ;
               rdfs:label ?label ;
               ns1:roleOf ?roleOf ;
               ns1:roleOf <https://example.org/affect.01> .
      ?roleSet ns1:subsumedUnder ?role .
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results) == 0:
    print("The given frame is not found among the tweets.")
else:
    for result in results:
        role = result[0]
        label = result[1]
        roleOf = result[2]
        print(f"The role: {role}")
        print(f"Label: {label}")
        print(f"RoleOf: {roleOf}")
        print()
