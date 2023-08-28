import json
from SPARQLWrapper import SPARQLWrapper, JSON

# loading the previously extracted fcg_output data
with open('./data/fcg_output.json', 'r') as f:
    fcg_output_list = json.load(f)


# creating a list to store the results of all frames from all tweets
combined_results_list = []

for output in fcg_output_list:
    if output.get("frameSet") is not None and output["frameSet"] is not None:
        frame_set = output["frameSet"]
        tweet_id = output["id"]
        tweet_text = output["text"]
        tweet_date = output["date"]
        tweet_polarity = output["polarity"]
        tweet_analysis = output["analysis"]
        tweet_subjectivity = output["subjectivity"]
        topic_list = output['topic'].split(', ')  # make topics list
        tweet_frames = {}

        results_list = []  # creating an empty list to store the results for each frame

        for frame in frame_set:
            frame_name = frame["frameName"]
            roles = frame["roles"]
            frame_roles = {}

            for role in roles:
                role_name = role["role"]
                role_string = role["string"]

                # storing the role and string in the frame_roles dictionary
                if role_name in frame_roles:
                    frame_roles[role_name].append(role_string)
                else:
                    frame_roles[role_name] = [role_string]

            # the SPARQL query to retrieve information about the frame from Framester
            sparql_template = r'''
                        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                        PREFIX tbox: <https://w3id.org/framester/framenet/tbox/>
                        SELECT DISTINCT ?frame ?hasInchoative
                        WHERE {
                                ?frame a tbox:Frame ;
                                tbox:hasInchoative ?hasInchoative ;
                                skos:closeMatch ?closeFrames .
                          FILTER regex(str(?closeFrames),"{frame_name}")
                        }
                        '''

            sparql_query = sparql_template.format(frame_name=frame_name, sent_number=1)
            sparql = SPARQLWrapper("http://etna.istc.cnr.it/framester2/sparql")
            sparql.setTimeout(300)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)

            sparql.addParameter('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
            results = sparql.query().convert()

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

        # appending the results_list to the combined_results_list
        combined_results_list.extend(results_list)

# writing the combined_results_list to a single JSON file
with open('../data/hasInchoative.json', 'w') as f:
    json.dump(combined_results_list, f, indent=4)