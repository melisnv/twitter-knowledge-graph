from rdflib import Graph, Namespace

graph = Graph()
graph.parse("graphs/twitterKnowledgeGraph.ttl", format="ttl") # enter the name of graph file

# Competency Question:
# What is the concept of a semantic frame and how does it capture the features associated with specific words?
query = """
    PREFIX ns1: <https://w3id.org/framester/framenet/abox/frame/>
    PREFIX ns2: <https://w3id.org/framester/framenet/tbox/>
    
    SELECT ?frame ?relationFrame
    WHERE {
        ?frame a ns1: ;
               ns2:hasFrameRelation ?relationFrame .
        FILTER (CONTAINS(STR(?frame), "scale"))   
    }

"""
results = graph.query(query)

# processing the query results programmatically to achieve the desired grouping and concatenation effect
for row in results:
    frame = row['frame'].split("/")[-1]
    relation = row['relationFrame'].split("/")[-1]

    print(f"frame:{frame}, related frame:{relation}")
    print("---------------------------")
