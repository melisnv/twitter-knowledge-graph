import json
from rdflib import Graph, Namespace

with open("../graphs/fcg_output.json", "r") as f:
    fcg_output = json.load(f)

frames_with_arg1 = []

for item in fcg_output:
    if item["frameSet"]:
        for frame in item["frameSet"]:
            for role in frame["roles"]:
                if role["role"] == "arg1":
                    frames_with_arg1.append(frame["frameName"])

print("\n")
print("FCG Part")
print(frames_with_arg1)

print("\n")
print("Framester Part")

graph = Graph()
graph.parse("graphs/26thJunedeneme.ttl", format="ttl")

# Defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Construct the query to retrieve only the frames (RoleOf) that have ARG1
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT ?roleOf WHERE {
      ?roleSet a <https://w3id.org/framester/pb/pbschema/RoleSet> ;
               ns1:subsumedUnder <https://w3id.org/framester/pb/pbschema/ARG1> ;
               ns1:roleOf ?roleOf .
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results) == 0:
    print("No frames found with ARG1.")
else:
    for result in results:
        roleOf = result[0]
        print(f"RoleOf: {roleOf}")