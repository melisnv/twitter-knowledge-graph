from rdflib import Graph, Namespace
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

graph = Graph()
graph.parse("graphs/1Julydeneme.ttl", format="ttl")

# defining the namespaces used in the graph
ns1 = Namespace("http://example.com/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# the GROUP_CONCAT function to concatenate the values of ?tweetId and ?closeMatchOf separated by commas within each group.
# the GROUP BY clause ensures that each unique combination of ?frame and ?comment is considered as a group.
query = """
    PREFIX ns1: <http://example.com/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?frame ?comment (GROUP_CONCAT(?tweetId; SEPARATOR=", ") AS ?tweetIds) (GROUP_CONCAT(?closeMatchOf; SEPARATOR=", ") AS ?closeMatchOfs)
    WHERE {{
      ?frame a ns1:Frame ;
             rdfs:label ?frameLabel ;
             ns1:frameOf ?frameNumber ;
             rdfs:comment ?comment ;
             ns1:closeMatchOf ?closeMatchOf .

      BIND(REPLACE(STRBEFORE(STRAFTER(STR(?frameNumber), "/FrameNumber/"), "/"), "/.*", "", "i") AS ?tweetId)
    }}
    GROUP BY ?frame ?comment
    """

results = graph.query(query, initNs={"ns1": ns1, "rdfs": rdfs})

query_results = []
# the query results
for result in results:
    frame = result[0]
    comment = result[1]
    tweetId = result[2]
    closeMatchOf = result[3]
    #print(f"frame: {frame}, comment: {comment}, tweetId: {tweetId},"f" closeMatchOf: {closeMatchOf}")
    #print("\n")

    query_results.append({
        "frame": frame,
        "comment": comment,
        "tweetIds": tweetId,
        "closeMatchOfs": closeMatchOf
    })

    # Extract comments from the query results
    comments = [result["comment"] for result in query_results]

    # Create TF-IDF vectors for the comments
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(comments)

    # Calculate cosine similarity scores between comments
    similarity_scores = cosine_similarity(tfidf_matrix)

    # Find the indices of the most similar comments
    most_similar_indices = []
    for i in range(len(comments)):
        similarity_scores[i, i] = 0  # Set self-similarity to 0
        most_similar_index = similarity_scores[i].argmax()
        most_similar_indices.append((i, most_similar_index))

    # Display the comments with the highest similarity scores
    for index_pair in most_similar_indices:
        index1, index2 = index_pair
        similarity_score = similarity_scores[index1, index2]

        comment1 = comments[index1]
        comment2 = comments[index2]

        print(f"Comment 1: {comment1}")
        print(f"Comment 2: {comment2}")
        print(f"Similarity Score: {similarity_score}")
        print("------------------")