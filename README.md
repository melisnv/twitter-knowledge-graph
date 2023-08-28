# Enhancing Twitter Data through Framester's Semantic Frames: Building and Enriching a Knowledge Graph

Analyzing social media texts is a pivotal area of research, with language's depth playing a crucial role. However, the intricate nature of language presents a significant challenge for contemporary natural language processing methods. Thus, the application of semantic frame analysis emerges as a vital tool for enhancing text analysis through linguistic understanding.

This master's thesis focuses on enriching the exploration of diverse perspectives and political narratives within social media texts. This enrichment is accomplished by employing semantic frame analysis, a method that delves into how linguistic structures trigger the activation of conceptual frames. Subsequently, the thesis investigates the integration of these activated frames into a comprehensive semantic analysis.

The analysis commences by extracting semantic frames from Twitter data, utilizing the Fluid Construction Grammar Editor. These extracted frames are then combined by harnessing a SPARQL query to access Framester, a knowledge graph amalgamating various linguistic resources like PropBank, FrameNet, WordNet, and VerbNet. The culmination of this process involves generating a knowledge graph that represents the derived insights.

Through this research, a deeper understanding of social media texts, their underlying frames, and the connections between linguistic components is achieved, thereby contributing to the advancement of social media text analysis.


## Getting Started

Follow these steps to run the program on your local machine:

1. **Clone the Repository** :

   Start by cloning this repository to the local machine using the following command:

   ```bash
   git clone git@github.com:melisnv/twitter-knowledge-graph.git
   ```
2. **Navigate to the Directory** :

   Move into the project directory:

   ```bash
   cd twitter-knowledge-graph
   ```
3. **Install Dependencies** :

   Install the project dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the required packages specified in the `requirements.txt` file.
4. **Run the Program in Sequence** : Run the program files in the specified sequence to achieve the desired functionality.

   ## How to Run the Code

   Follow these steps to run the code and perform the necessary data processing, analysis, and knowledge graph creation.

   ### 1. Data Preparation


   - Make sure you have the `json_data_processing.py` file and the Twitter JSON data available in the same directory.
   - Run `json_data_processing.py` to bring the Twitter JSON data into a single Pandas DataFrame structure.

   ### 2. Topic Modeling and Sentiment Analysis

   - Run `topic_sentiment_analysis.py` to perform topic modeling and sentiment analysis on the Twitter data.
   - This script will also clean the data for further processing.

   ### 3. Semantic Frame Extraction

   - Execute `fcg_data_extractor.py` to extract semantic frames from the processed data.

   ### 4. Automated Script Execution

   - Run `automated_script_runner.py` to automatically execute Framester queries.
   - This step populates Framester queries with relevant data.

   ### 5. JSON File Generation

   - Execute `merge_json_files.py` to combine the output from Framester queries with other JSON files.
   - The combined data is saved in a JSON file.

   ### 6. Knowledge Graph Creation

   - Finally, run `build_knowledge_graph.py` to create a knowledge graph using the JSON file obtained from the previous step.
   - The resulting knowledge graph contains enriched information from the processed data.
