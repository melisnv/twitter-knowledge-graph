from rdflib import Graph, Namespace
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

graph = Graph()
graph.parse("graphs/1stJuly2.ttl", format="ttl")

# defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?comment
    WHERE {
      ?frame a ns1:Frame ;
             rdfs:label ?label ;
             rdfs:comment ?comment .
    }
    """

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs})
query_results = []

# the query results
for result in results:
    label = result[0]
    comment = result[1]
    print(f"label: {label}, comment: {comment}")

    query_results.append({
        "comment": comment,
        "label": label,
    })

# Extract comments from query results
comments = [result["comment"] for result in query_results]

# Apply TF-IDF vectorization to comments
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(comments)

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Assign similarity scores to comment pairs
for i in range(len(comments)):
    comment1 = comments[i]
    label1 = query_results[i]["label"]

    if i + 1 >= len(comments):
        break

    print(f"Comment 1 - label: {label1}, comment: {comment1}")
    print("Similarity Scores:")

    for j in range(i + 1, len(comments)):
        comment2 = comments[j]
        label2 = query_results[j]["label"]

        similarity_score = cosine_sim[i, j]

        print(f"Comment 2 - label: {label2}, comment: {comment2}")
        print(f"Similarity score: {similarity_score:.4f}\n")

