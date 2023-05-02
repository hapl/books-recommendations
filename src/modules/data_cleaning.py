
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
import re

#Apply Data Tokenization, lower case, filtering and lemmatization
def data_cleaning_reviews(df):
    """
    Recieve dataframe and process text field "Review_text_clean" do lemmatization
    tokenize, remove stop words, remove puntuation and numbers from text.
    """
    df1 = df.copy()
    stop_words = set(stopwords.words('english'))
    punct = string.punctuation
    lemmatizer = nltk.WordNetLemmatizer()
    #Remove punctuation 
    def remove_punctuation(text):
        return text.translate(punct)
    #Preprocess text
    def preprocess(text):
        # Remove any mathematical symbols or operators
        text = re.sub(r"[\^\/\*\+\-\=\(\)]", "", text)
        text = re.sub(r"[^a-zA-Z\s,.]","", text)
        #Remove numbers
        text = re.sub(r"\d+", "", text)
        text = text.lower()
        return text
#    df1['review_text_clean'] = df1['review_text'].astype(str).apply(lambda x:[lemmatizer.lemmatize(word) 
#                                                              for word in word_tokenize(preprocess(x)) 
#                                                              if word.lower() not in stop_words and word.lower() not in punct])
    df1['review_text_clean'] = df1['review_text'].astype(str).apply(lambda x:[lemmatizer.lemmatize(word) 
                                                              for word in remove_punctuation(preprocess(x)).split() 
                                                              if word not in stop_words]) 
    return df1

def data_cleaning_books(df):
    """
    Recieve dataframe and process text field "Book description" do lemmatization
    tokenize, remove stop words, remove puntuation and numbers from text.
    """
    df1 = df.copy()
    stop_words = set(stopwords.words('english'))
    punct = str.maketrans('', '', string.punctuation) #string.punctuation
    lemmatizer = nltk.WordNetLemmatizer()
    #Remove punctuation
    def remove_punctuation(text):
        return text.translate(punct)
    #Preprocess text
    def preprocess(text):
        # Remove any mathematical symbols or operators
        text = re.sub(r"[\^\/\*\+\-\=\(\)]", "", text)
        text = re.sub(r"[^a-zA-Z\s,.]","", text)
        #Remove numbers
        text = re.sub(r"\d+", "", text)
        text = text.lower()
        return text
#    df1['description_text_clean'] = df1['description'].astype(str).apply(lambda x:[lemmatizer.lemmatize(word) 
#                                                              for word in word_tokenize(preprocess(x)) 
#                                                              if word.lower() not in stop_words and word.lower() not in punct])
    df1['description_text_clean'] = df1['description'].astype(str).apply(lambda x:[lemmatizer.lemmatize(word) 
                                                              for word in remove_punctuation(preprocess(x)).split() 
                                                              if word not in stop_words])
    return df1