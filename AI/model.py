import pandas as pd
import numpy as np
import nltk, string
import pickle
import dill
from sklearn.feature_extraction.text import TfidfVectorizer

# nltk.download('punkt') # if necessary...

data_path = "combined.csv"
pd.set_option('display.max_colwidth', None)

model = TfidfVectorizer()

def preprocess_data(data_path, sample_size):

    # Read the data from specific path
    data = pd.read_csv(data_path, index_col=0)

    # Drop articles without Abstract
    data = data.dropna(subset = ['abstract']).reset_index(drop = True)

    # Get "sample_size" random articles
    #data = data.sample(sample_size)[['abstract']]

    return data

def cosine_sim(text1, text2):
    tfidf = model.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

def is_plagiarism(similarity_score, plagiarism_threshold):

    is_plagiarism = False
    if(similarity_score >= plagiarism_threshold):
        is_plagiarism = True

    return is_plagiarism

def run_plagiarism_analysis(query_text, data, plagiarism_threshold=0.8):

    top_N=3

    # Run similarity Search
    data["similarity"] = data["abstract"].apply(lambda x: cosine_sim(query_text, x))

    similar_articles = data.sort_values(by='similarity', ascending=False)[0:top_N+1]
    formated_result = similar_articles[["abstract", "similarity"]].reset_index(drop = True)
    similarity_score = formated_result.iloc[0]["similarity"] 
    similarity_percentage = str(round(similarity_score *100)) + '%'
    most_similar_article = formated_result.iloc[0]["abstract"] 
    is_plagiarism_bool = is_plagiarism(similarity_score, plagiarism_threshold)


    plagiarism_decision = {'similarity_score': similarity_score, 
                           'similarity_percentage': similarity_percentage,
                            'is_plagiarism': is_plagiarism_bool,
                            'most_similar_article': most_similar_article, 
                            'article_submitted': query_text
                        }
    return plagiarism_decision
    #return formated_result


def predict(new_incoming_text, data_path):
    source_data = preprocess_data(data_path, 20000)
    decision=run_plagiarism_analysis(new_incoming_text, source_data, plagiarism_threshold=0.5)
    return decision
pickle.dump(predict, open('model.pkl','wb'))