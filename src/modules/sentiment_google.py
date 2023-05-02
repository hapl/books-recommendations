from transformers import pipeline
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import string
import pandas as pd
import os
google_key = os.environ["GOOGLE_KEY"]
import requests

# Download the necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Define the tokenizer and lemmatizer
tokenizer = word_tokenize
lemmatizer = WordNetLemmatizer()

sentiment_pipeline = pipeline("sentiment-analysis", truncation=True)

# Define a function to tokenize and lemmatize the text
def tokenize_and_lemmatize(text):
   #     df1 = df.copy()
    #stop_words = set(stopwords.words('english'))
    punct = string.punctuation
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    #Preprocess text
    def preprocess(text):
        #remove_punctuation(text):
        text = text.translate(punct)
        # Remove any mathematical symbols or operators
        text = re.sub(r"[\^\/\*\+\-\=\(\)]", "", text)
        text = re.sub(r"[^a-zA-Z\s,.]","", text)
        #Remove numbers
        text = re.sub(r"\d+", "", text)
        text = text.lower()
        return text
    text = preprocess(text)
    # Tokenize the text into words
    tokens = tokenizer(text)

   #' '.join([lemmatizer.lemmatize(token) for token in tokens])
    # Lemmatize each word and return as a string
    return ' '.join([lemmatizer.lemmatize(token) for token in tokens if token not in stop_words])

def sentiment_analysis(df):
    df['sentiment'] = df['review_clean'].apply(sentiment_pipeline)
    # Extract the sentiment label and score from the pipeline output
    df['sentiment_label'] = df['sentiment'].apply(lambda x: x[0]['label'])
    df['sentiment_score'] = df['sentiment'].apply(lambda x: x[0]['score'])
    return df

def add_data_sentiment(df):
    # Group by book_id and sentiment_label and count the number of reviews
    counts = df.groupby(['book_id', 'sentiment_label']).size().reset_index(name='count')
    # Pivot the data to reshape it into a table with columns for positive and negative counts
    pivot_table = pd.pivot_table(counts, values='count', index='book_id', columns='sentiment_label', fill_value=0)
    # Add columns for total and percentage of positive and negative reviews
    pivot_table['total_reviews'] = pivot_table.sum(axis=1)
    pivot_table['% positive'] = pivot_table['POSITIVE'] / pivot_table['total_reviews']
    pivot_table['% negative'] = pivot_table['NEGATIVE'] / pivot_table['total_reviews']
    return pivot_table

def get_final_data(df1,df2):
    df_books_data = df2[['book_id','title','name','average_rating', 'image_url']]
    df_final = pd.merge(df1,df_books_data,on='book_id',how='left')
    return df_final


def clickable(value):
    return '<a target="_blank" href="{}">Google Books Details</a>'.format(value, value)

def show_cover(value):
    return '<img src="{}" width=60></img>'.format(value)


# Define a function to get the google books api link for a book
def get_google_link(title, author):
    # Format the search query
    query = f"{title} {author} buy"

    # Make a request to the Google Books API
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": query, "key": google_key}
    )

    # Parse the response JSON
    data = response.json()

    # Extract the buy link from the response, if it exists
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["volumeInfo"].get("infoLink", "")
    else:
        return ""
    
def format_output_table(df_final_data):
        df_final_data = df_final_data.rename(columns={'book_id':'BookID','NEGATIVE':'NegativeReviews','POSITIVE':'PositiveReviews','total_reviews':'TotalReviews',
                               'title':'BookTitle', 'name':'AuthorName','average_rating':'AverageRating','image_url':'Cover','Buy Link':'GoogleAPI'})
        return df_final_data


