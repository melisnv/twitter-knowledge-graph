import json
import time
from SPARQLWrapper import SPARQLWrapper, JSON

#with open('data/lastQueryResults/fcg_output_denemehasFrameRelation.json', 'r') as f:
#    fcg_output_list = json.load(f)

with open('filtered_json.json', 'r') as f:
    fcg_output_list = json.load(f)

# creating an empty list to store the results of all frames from all tweets
combined_results_list = []

for output in fcg_output_list:
    frame_set = output.get("frameSet")
    if frame_set is not None and len(frame_set) > 0:
        tweet_id = output.get("id")
        tweet_text = output.get("text")
        tweet_date = output.get("date")
        tweet_polarity = output.get("polarity")
        tweet_analysis = output.get("analysis")
        tweet_subjectivity = output.get("subjectivity")
        topic_list = output.get("topic", "").split(", ")
        tweet_frames = {}

        results_list = []  # create an empty list to store the results for each frame

        for frame in frame_set:
            frame_name = frame.get("frameName")
            roles = frame.get("roles")
            frame_roles = {}

            for role in roles:
                role_name = role.get("role")
                role_string = role.get("string")

                # store the role and string in the frame_roles dictionary
                if role_name in frame_roles:
                    frame_roles[role_name].append(role_string)
                else:
                    frame_roles[role_name] = [role_string]

                print(
                    f"Date: {tweet_date}, Tweet ID: {tweet_id}, Tweet: {tweet_text}, "
                    f"Frame: {frame_name}, Role: {role_name}, String: {role_string}, "
                    f"Topic: {topic_list}, Subjectivity: {tweet_subjectivity}, "
                    f"Polarity: {tweet_polarity}, Analysis: {tweet_analysis}"
                )

            # the SPARQL query to retrieve information about the frame from Framester
            sparql_template = r'''
                        PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        
                        SELECT DISTINCT ?frame ?sameAs ?label
                        WHERE {{
                            ?frame a tbox:Frame ;
                            owl:sameAs ?sameAs ;
                            skos:closeMatch ?closeFrames ;
                            rdfs:label ?label .
                          FILTER regex(str(?closeFrames), "{frame_name}")
                          FILTER (?sameAs = ?targetSameAs)
                        }}
                    '''

            sparql_query = sparql_template.format(frame_name=frame_name, sent_number=1)
            sparql_endpoint = "http://localhost:7200/repositories/framester"  # GraphDB endpoint
            agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' # User-Agent
            sparql = SPARQLWrapper(sparql_endpoint, agent=agent)
            sparql.setTimeout(300)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)

            #results = sparql.query().convert()
            try:
                results = sparql.query().convert()
            except Exception as e:
                print(f"Error executing SPARQL query for frame {frame_name}: {str(e)}")
                print("Skipping to the next frame...")
                time.sleep(1)  # wait for 1 second before moving to the next iteration
                continue

            results_with_frame_name = {
                "frame_name": frame_name,
                "tweet_id": tweet_id,
                "text": tweet_text,
                "date": tweet_date,
                "subjectivity": tweet_subjectivity,
                "polarity": tweet_polarity,
                "analysis": tweet_analysis,
                "frame_roles": frame_roles,
                "topics": topic_list,
                "results": results
            }
            results_list.append(results_with_frame_name)

        combined_results_list.extend(results_list)

# writing the combined_results_list to a single JSON file
with open('data/lastQueryResults/sameAs2000.json', 'w') as f:
    json.dump(combined_results_list, f, indent=4)
