from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/26thJunedeneme.ttl", format="ttl")

# Defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# define the desired frame name (for example Statement etc.)
frame_name = "Statement"

# Specify the frame URI as a variable
frame_uri = f"<https://w3id.org/framester/framenet/abox/frame/{frame_name}>"

# Construct the query with the frame URI variable
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?relatedFrame WHERE {
      """ + frame_uri + """ ns1:isRelated ?relatedFrame .
    }
"""

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs, "xsd": xsd})

if len(results) == 0:
    print("The given frame is found among the tweets.")
else:
    for result in results:
        related_frame = result[0]
        print(f"Related Frames: {related_frame}")
