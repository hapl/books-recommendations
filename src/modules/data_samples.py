# Create data samples

import pandas as pd
import numpy as np
import random

def get_data():
    """
    Funtion to read all the books in csv file and create a random sample with 5% of the data.
    """
    #Create samples
    books_file = ('../data/book_authors.csv')
    df_books_all = pd.read_csv(books_file)
    books_filtered = df_books_all[df_books_all['language_code'].isin(['--', 'eng', 'en-CA', 'en-GB', 'en-US', 'en', 'enm', np.nan])]
    #n = sum(1 for line in open(books_file))-1
    pct = 0.05 #books sample size in percentage
    #skip_values = sorted(random.sample(range(1,n+1),n-s))
    #pd.read_csv(books_file, skiprows=lambda i: i>0 and random.random() > pct)
    df_books_sample = books_filtered.sample(frac=pct)
    df_book_reviews = get_book_reviews(df_books_sample)
    df_book_author  = get_book_authors(df_books_sample)
    df_books_genre  = get_book_genres(df_books_sample)
    return df_books_sample, df_book_author, df_book_reviews, df_books_genre 

def get_book_reviews(df):
    """
    Funtion to read all the reviews from csv and filter only the ones coming from the books dataframe sample.
    It returns a dataframe with all the reviews related to books in the book sample.
    """
    review_file = ('../data/book_reviews.csv')
    df_review_initial = pd.read_csv(review_file)
    df_review_initial.dropna(subset=['book_id'], inplace=True)
    df_reviews_sample = df_review_initial[df_review_initial["book_id"].astype(int).isin(df["book_id"].astype(int))]
    return df_reviews_sample

def get_book_authors(df):
    """
    Funtion to read all the authors from csv and filter only the ones coming from the books dataframe sample.
    It returns a dataframe with all the authors in the book sample.
    """
    author_file = ('../data/authors.csv')
    df_author_initial = pd.read_csv(author_file)
    df_author_initial.dropna(subset=['author_id'], inplace=True)
    df_authors_sample  = df_author_initial[df_author_initial["author_id"].astype(int).isin(df["author"].astype(int))]
    df_authors_sample.reset_index(drop=True, inplace=True)
    return df_authors_sample

def get_book_genres(df):
    """
    Funtion to read all the genres from csv and filter only the ones coming from the books dataframe sample.
    It returns a dataframe with all the genres in the book sample.
    """
    genres_file = ('../data/genres_processed.csv')
    df_genres_initial = pd.read_csv(genres_file)
    df_genres_books = df_genres_initial[df_genres_initial["book_id"].astype(int).isin(df["book_id"].astype(int))]
    df_genres_sample = get_genres_processing(df_genres_books)
    df_genres_sample.reset_index(drop=True, inplace=True)
    return df_genres_sample 

def get_genres_processing(df):
    """
    Get genres list for only the books on the sample because the genres file have millions 
    of entries and it is not worth it to have it all. this function split all the values in the dictionary list.
    """
    # create an empty dataframe to store the results
    df_tmp = pd.DataFrame(columns=['book_id', 'genres'])
    df_genres_processed = pd.DataFrame(columns=['book_id', 'genres'])

    for index, row in df.iterrows():
        genre_dict = eval(row['genres'])
        for genre, count in genre_dict.items():
            new_row = {'book_id': row['book_id'], 'genres': genre}
            df_tmp = pd.concat([df_tmp, pd.DataFrame([new_row])], ignore_index=True)
    #clean leftover commas after dictionary processing. Could not process in the above code it caused formatting issues.
    df_genres_processed = get_genres_clean_processing(df_tmp) 

    return df_genres_processed

def get_genres_clean_processing(df_tmp):
    """
    Process all the commas and list values left after first processing of genres list.
    """
#split all the comma values left after the first processing.
    for index, row in df_tmp.iterrows():
        genres_list = row['genres'].split(', ')
        new_rows = [{'book_id': row['book_id'], 'genres': genre} for genre in genres_list]
        new_df2 = pd.concat([new_df2, pd.DataFrame(new_rows)], ignore_index=True)

    # sort the new dataframe by book_id
    new_df2 = new_df2.sort_values('book_id')

    # reset the index of the new dataframe
    new_df2 = new_df2.reset_index(drop=True)
    return new_df2