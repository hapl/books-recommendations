import pandas as pd
import json
import gzip
from collections import defaultdict 

#load files
def load_data(file_name):
    #based on the funtion documented on https://github.com/MengtingWan/goodreads by the creators of the dataset

    data = []
    with gzip.open(file_name) as fin:
        for l in fin:
            d = json.loads(l)
            data.append(d)
    return data

def book_data(file_name):
 data = []
 c = 0
 with gzip.open(file_name) as f:
    for i,line in enumerate(f):
      j = json.loads(line)
      if (j['text_reviews_count'] == '' or j['average_rating'] == '' or j['description'] == '' or j['num_pages'] == '' or j['publication_year'] == '' or j['image_url'] == '' or j['book_id'] == '' or j['ratings_count'] == '' or  j['title'] == ''):
        continue
      try: # try to access the first element of the authors list
        j['author'] = j['authors'][0]['author_id']
      except IndexError: # catch the error if it occurs
        continue
      data.append(j)
    return data

def load_data_reviews(file_name,df_books):
    
    count = 0
    data = []
    with gzip.open(file_name) as fin:
        for i,line in enumerate(fin):
            d = json.loads(line)
            count += 1
            d['book_id'] = int(d['book_id'])
            if d['book_id'] in df_books['book_id'].values:
                data.append(d)
    return data

def fix_book_genres(df_books,df_genres):
   #get books without genre
    books_without_genres = []
    for i, k in df_genres.iterrows():
      if k["genres"] == {}:
        books_without_genres.append(k["book_id"])
    
    df_book_final = df_books[~df_books["book_id"].astype(int).isin(books_without_genres)]
    df_genres_final = df_genres[~df_genres["book_id"].isin(books_without_genres)]
    return df_book_final,df_genres_final


def organize_genres(df):
  df_genres = pd.DataFrame(columns=["genre_id", "genre"])
  df_genres_books = pd.DataFrame(columns=["genre_id","book_id"])
  c = 0
  unique_genres = defaultdict()
  for i, k in df.iterrows():
      #c+=1
      #print(c)
      g = list(k["genres"])[0]
      g_1 = g.split(',')
      for _, g_ in enumerate(g_1):
        g_2 = g_.replace(" ", "").split(',')
        for _, g__ in enumerate(g_2):
          if (g__ not in unique_genres):
            unique_genres[g__] = []
          else:
            unique_genres[g__].append(k["book_id"])
      #if (head is not None) and (c > head):
       # break
  key_genres = [key for key in unique_genres.keys() if key != 'default']
  return unique_genres, key_genres

def process_genre_id(unique_genres):
  df_genres = pd.DataFrame(columns=["genre_id", "genre"])
  for i,k in enumerate(unique_genres.keys()):
    df_genres.append({'genre_id':i, 'genre':k}, ignore_index=True)
  return df_genres

def process_genre_id(unique_genres):
  df_genres = pd.DataFrame(columns=["genre_id", "genre"])
  for i,k in enumerate(unique_genres.keys()):
    # assign the values to the row with index i
    df_genres.loc[i, "genre_id"] = i
    df_genres.loc[i, "genre"] = k
  return df_genres


