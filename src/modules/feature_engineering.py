import pandas as pd
import numpy as np



def read_data_sample():
    df_books_sample     = pd.read_csv('../data/sample_data/processed/books_sample.csv')
    df_authors_sample   = pd.read_csv('../data/sample_data/processed/authors_sample.csv')
    df_reviews_sample   = pd.read_csv('../data/sample_data/processed/reviews_sample.csv')
    df_genres_sample    = pd.read_csv('../data/sample_data/processed/genres_sample.csv')
    return df_books_sample, df_authors_sample, df_reviews_sample, df_genres_sample 

