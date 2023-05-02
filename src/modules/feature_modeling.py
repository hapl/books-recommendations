import pandas as pd
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import KNNBaseline
from surprise import SVD
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering
from surprise.accuracy import rmse
from surprise import accuracy
from surprise.model_selection import train_test_split
import sklearn

import warnings


def read_data_sample():
    df_books_sample     = pd.read_csv('../data/sample_data/processed/books_sample.csv')
    df_authors_sample   = pd.read_csv('../data/sample_data/processed/authors_sample.csv')
    df_reviews_sample   = pd.read_csv('../data/sample_data/processed/reviews_sample.csv')
    df_genres_sample    = pd.read_csv('../data/sample_data/processed/genres_sample.csv')
    return df_books_sample, df_authors_sample, df_reviews_sample, df_genres_sample 


#def cosine_similarity_cal(df):
#    """Calculate the cosine of similarity for the corpus
#    """
#    tfid_vectorizer = TfidfVectorizer()
#    tfidf_matrix = tfid_vectorizer.fit_transform(df['corpus'])
#    cosine_sim_cal = cosine_similarity(tfidf_matrix, tfidf_matrix)
#    df_cosine_sim_cal = pd.DataFrame(cosine_sim_cal)
#    return df_cosine_sim_cal, cosine_sim_cal



def remove_apostrophe(word):
    """ Removes apostrophes from a word
    """
    # Create a mapping table for apostrophes
    apostrophe_table = str.maketrans('', '', "'[]")
    return word.translate(apostrophe_table)

def process_main_features(df,version):
    if version == 'A':
        main_features = ['title', 'author','name','genres', 'description_text_clean', 'num_pages']
    else:
        main_features = ['book_id','title','author','name','genres', 'description_text_clean', 'num_pages']
    df_books_final = df.loc[:, main_features]
    df_books_final = df_books_final.rename(columns={'name' : 'author_name'})
    df_books_final['keywords'] = df_books_final['description_text_clean'].apply(lambda x: ' '.join(list(set(remove_apostrophe(word) for word in x.split()))))
    return df_books_final

def additional_cleaning_books(df_books_final_book_id):
    df_books_final_book_id["title_clean"] = df_books_final_book_id['title'].str.replace("[^a-zA-Z0-9 ]", "", regex=True).str.lower()
    df_books_final_book_id["title_clean"] = df_books_final_book_id['title'].str.replace("\s+", " ", regex=True)
    df_books_final_book_id.drop(columns=['title'], inplace=True)
    df_books_final_book_id= df_books_final_book_id.rename(columns={'title_clean':'title'})
    return df_books_final_book_id

def prepare_corpus(df_books_final):
    """Prepare corpus and adjust data for recommenders
    """
    df_books_final['corpus'] = (pd.Series(df_books_final[['genres', 'keywords']].fillna('').values.tolist()).str.join(' '))
    df_books_final["title_clean"] = df_books_final['title'].str.replace("[^a-zA-Z0-9 ]", "", regex=True).str.lower()
    df_books_final["title_clean"] = df_books_final['title'].str.replace("\s+", " ", regex=True)
    return df_books_final

def cosine_similarity_cal(df,column):
    """Calculate the cosine of similarity based on the column received as parameter
    """
    tfid_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfid_vectorizer.fit_transform(df[column])
    cosine_sim_cal = cosine_similarity(tfidf_matrix, tfidf_matrix)
    df_cosine_sim_cal = pd.DataFrame(cosine_sim_cal)
    return df_cosine_sim_cal, cosine_sim_cal

def cosine_recommendations(title,titles,title_ind,cosine_sim_c):
    """ cosine of recomentations based on title and indices
        title: book to analyze for recommender
        titles: list of titles
        indices of titles
        and the array of cosine of similarity
    """
    idx = title_ind[title]
    sim_scores = list(enumerate(cosine_sim_c[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

def get_recommendation(title,cosine_s,df_book_map,df_books_final,top_n=11):
    """
    Get recommendations based on book map and clusters
    """
    
    # get index from input title
    book_id = df_book_map[title]
    
    # calculate similarity score, sort value descending and get top_n book
    sim_score = list(enumerate(cosine_s[book_id]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    sim_score = sim_score[:top_n]
    
    # get book index from top_n recommendation
    book_indices = [score[0] for score in sim_score]
    scores = [score[1] for score in sim_score]
    top_n_recommendation = df_books_final[['title', 'author_name', 'genres']].iloc[book_indices]
    top_n_recommendation['genres'] = top_n_recommendation['genres'].apply(lambda x: x.split())
    top_n_recommendation['score'] = scores
    return top_n_recommendation.iloc[1:]

def compare_algorithm(data):
    """Compare SVD, SVDpp and NMF
    """
    benchmark = []
    #compare algorithm
    for algorithm in [SVD(), SVDpp(), NMF()]:
        # Perform cross validation
        results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=False)

        #Get results
        tmp = pd.DataFrame.from_dict(results).mean(axis=0)
        tmp = pd.concat([tmp, pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm'])], axis=0)

        benchmark.append(tmp)
    df_surprise_results = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse')
    return df_surprise_results