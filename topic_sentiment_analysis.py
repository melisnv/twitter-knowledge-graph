import re
import spacy
import pandas as pd
import contractions
from textblob import TextBlob
from nltk.corpus import stopwords
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from json_data_processing import process_json_data

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', None)  # Auto-adjust width


def preprocess_text(text):
    # removing URLs
    url_regex = re.compile(r'http\S+')
    text = url_regex.sub('', text)
    # expanding contractions
    text = contractions.fix(text)
    # removing special characters and digits
    text = re.sub('[^a-zA-Z]', ' ', text)
    # converting to lowercase
    text = text.lower()
    # tokenizing text
    tokens = word_tokenize(text)
    # removing stopwords
    stop_words = stopwords.words('english')
    tokens = [word for word in tokens if word not in stop_words]
    # lemmatizing tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # joining tokens back into a single string
    text = ' '.join(tokens)

    return text


def get_dominant_topic(model, corpus, texts):
    # getting main topic in each document
    topic_keywords = model.show_topics(formatted=False)
    dominant_topic = []
    for i, row in enumerate(model[corpus]):
        row = sorted(row, key=lambda x: x[1], reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # get dominant topic
                topic = topic_keywords[topic_num]
                words = [word for word, prop in topic[1]]
                topic_name = ', '.join(words)
                dominant_topic.append(topic_name)
            else:
                break
    return dominant_topic


def getSubjectivity(review):
    return TextBlob(review).sentiment.subjectivity


def getPolarity(review):
    return TextBlob(review).sentiment.polarity


# function to analyze the reviews
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def main():
    # loading the English language model for spaCy
    nlp = spacy.load("en_core_web_sm")

    # defining the directory where the JSON files are located
    json_dir = 'data/'
    # the function to process JSON data
    data = process_json_data(json_dir)

    # preprocessing to clean the tweets
    data['cleaned_text'] = data['text'].apply(preprocess_text)

    # applying preprocessing function to 'text' column of DataFrame
    data['cleaned_text'] = data['text'].apply(preprocess_text)
    # tokenizing the text in the 'text' column of your dataframe
    texts = [[token.text for token in nlp(text)] for text in data['cleaned_text']]
    # creating a dictionary of unique words from the tokenized texts
    dictionary = Dictionary(texts)
    # converting the tokenized texts to bag-of-words format using the dictionary
    corpus = [dictionary.doc2bow(text) for text in texts]
    # training an LDA model on the corpus
    lda_model = LdaModel(corpus=corpus, num_topics=5, id2word=dictionary)
    # assigning the topics
    data['topic'] = get_dominant_topic(lda_model, corpus, data['cleaned_text'])

    # applying the sentiment analysis to the data
    data['Subjectivity'] = data['cleaned_text'].apply(getSubjectivity)
    data['Polarity'] = data['cleaned_text'].apply(getPolarity)
    data['analysis'] = data['Polarity'].apply(getAnalysis)
    data["subjectivity"] = data["Subjectivity"].apply(lambda x: round(x, 2))
    data["polarity"] = data["Polarity"].apply(lambda x: round(x, 2))

    # cleaning the columns in order to remove the unnecessary features
    data = data[['id', 'text', 'created_at', 'cleaned_text', 'topic', 'analysis', 'subjectivity', 'polarity']]
    # saving the processed data to a CSV file
    data.to_csv('twitter_data.csv', index=False)  # Set index=False to exclude index column


if __name__ == "__main__":
    main()
