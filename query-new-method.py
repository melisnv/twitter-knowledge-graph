from rdflib import Graph, Dataset
from rdflib.plugins.stores.hdt import HDTStore

store = HDTStore("framenet.hdt")
graph = Graph(store, identifier="http://example.org/frame")


query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fn: <http://www.w3.org/2005/11/ftf-ontology-ns#>

SELECT ?frame ?definition
WHERE {
    ?frame rdf:type fn:Frame .
    ?frame fn:definition ?definition .
}
"""

# executing the query
results = graph.query(query)


for row in results:
    print(row)
