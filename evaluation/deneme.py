from rdflib import Graph, URIRef, RDF, RDFS, Namespace

# Load the knowledge graph from the TTL file
graph = Graph()
graph.parse("graphs/15thJune3.ttl", format="ttl")

# Define the namespaces used in the graph
ns1 = URIRef("http://example.com/")
rdf = RDF
rdfs = RDFS

# Perform advanced querying
# Query 1: Find all frames related to the topic "libs"
topic = URIRef("https://example.org/Topic/libs")
query1 = """
    SELECT ?frame WHERE {
        ?frame ns1:isAbout ?topic .
    }
"""
results1 = graph.query(query1, initNs={"ns1": ns1}, initBindings={"topic": topic})
print("Frames related to 'libs':")
for row in results1:
    print(row["frame"])

# Query 2: Find the labels of frames similar to "Arriving"
frame = URIRef("http://premon.fbk.eu/resource/fn17-arriving")
query2 = """
    SELECT ?label WHERE {
        ?frame a ns1:EquivalentClass ;
               rdfs:label ?label ;
               ns1:similarConceptOf ?frame .
    }
"""
results2 = graph.query(query2, initNs={"ns1": ns1, "rdfs": rdfs}, initBindings={"frame": frame})
print("Labels of frames similar to 'Arriving':")
for row in results2:
    print(row["label"])

# Query 3: Find the topics associated with a specific frame number
frame_number = URIRef("https://example.org/1457054652197920770")
query3 = """
    SELECT ?topic WHERE {
        ?frame_number ns1:isAbout ?topic .
    }
"""
results3 = graph.query(query3, initNs={"ns1": ns1}, initBindings={"frame_number": frame_number})
print("Topics associated with frame number '1457054652197920770':")
for row in results3:
    print(row["topic"])

# Perform knowledge discovery
# Find all frames that have a frame relation
query4 = """
    SELECT DISTINCT ?frame WHERE {
        ?frame ns1:hasFrameRelation ?relation .
    }
"""
results4 = graph.query(query4, initNs={"ns1": ns1})
print("Frames with frame relations:")
for row in results4:
    print(row["frame"])