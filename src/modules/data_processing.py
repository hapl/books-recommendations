import pandas as pd
import json
import gzip
from collections import defaultdict 

#load files
def load_data(file_name):#, head = 500):
    #based on the funtion documented on https://github.com/MengtingWan/goodreads by the creators of the dataset
    count = 0
    data = []
    with gzip.open(file_name) as fin:
        for l in fin:
            d = json.loads(l)
            count += 1
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
      #for _,col in enumerate(cols_excluded):
    # del j[col]
      #if(j['authors'] != ''):
      #  j['author'] = j['authors'][0]['author_id']
      try: # try to access the first element of the authors list
        j['author'] = j['authors'][0]['author_id']
      except IndexError: # catch the error if it occurs
        continue
      #  print("No author found for line", i)
      data.append(j)
      #c+=1
      #if (c == 10):
       # break
    return data

def load_data_reviews(file_name,df_books):#, head = 500):
    
    count = 0
    data = []
    with gzip.open(file_name) as fin:
        for i,line in enumerate(fin):
            d = json.loads(line)
            count += 1
            # convert d['book_id'] to int64
            d['book_id'] = int(d['book_id'])
            if d['book_id'] in df_books['book_id'].values:
                data.append(d)
           
            # break if reaches the 500th line
           # if (head is not None) and (count > head):
           #     break
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

def organize_genres(df, head = 500):
  df_genres = pd.DataFrame(columns=["genre_id", "genre"])
  df_genres_books = pd.DataFrame(columns=["genre_id","book_id"])
  c = 0
  unique_genres = defaultdict()
  for i, k in df.iterrows():
      c+=1
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
      if (head is not None) and (c > head):
        break
  key_genres = [key for key in unique_genres.keys() if key != 'default']
  return unique_genres, key_genres

def process_genre_id(unique_genres):
  df_genres = pd.DataFrame(columns=["genre_id", "genre"])
  for i,k in enumerate(unique_genres.keys()):
    #df_genres = 
    df_genres.append({'genre_id':i, 'genre':k}, ignore_index=True)
  return df_genres
#
#  for ge, k in unique_genres.items(): 
#    #print(ge)
#    #print(len(k))
#    g = df.loc[df["genre"] == ge]["genre_id"]
#    for _, book_id in enumerate(k):
#      df_genres_books = df_genres_books.append({'genre_id':int(g), 'book_id':book_id}, ignore_index=True)
#              # break if reaches the 500th line
# 
#  return df_genres_books, df_genres


#def fix_book_authors(df_books, df_authors):
#    authors = df_authors["author_id", "book_id", "name"]
#    for i, k in df_books.iterrows():
#      if k["author_id"] == df_books["author_id"]:
#         
#      for a in k["author_id"]:
#        authors["author_id"] = 
#        authors = authors.append
#  #Remove authors column
#    #df_books.drop(columns=["authors"], axis=1, inplace=True)
#    authors = authors[authors["author_id"].isin(df_authors["author_id"])]
#    return authors
#
#Organize data for books
#def books_data(data):
#    #data = json.loads(data)
#    df_shelves = []
#    df_authors = []
#    book_data = []
#    for sd in data:
#    #Orginize data
#        book_data.append({
#        'isbn':	                sd['isbn'],
#        'text_reviews_count':	sd['text_reviews_count'],
#    #    'series':	            sd['series'],
#        'country_code':	        sd['country_code'],
#        'language_code':	    sd['language_code'],
#    #    'popular_shelves':	    sd['popular_shelves'],
#        'asin':	                sd['asin'],
#     #   'is_ebook':	            sd['is_ebook'],
#        'average_rating':	    sd['average_rating'],
#     #   'kindle_asin':	        sd['kindle_asin'],
#      #  'similar_books':	    sd['similar_books'],
#        'description':	        sd['description'],
#       # 'format':	            sd['format'],
#       # 'link':	                sd['link'],
#       # 'authors':	            sd['authors'],
#        'publisher':	        sd['publisher'],
#      #  'num_pages':	        sd['num_pages'],
#      #  'publication_day':	    sd['publication_day'],
#        'isbn13':	            sd['isbn13'],
#       # 'publication_month':	sd['publication_month'],
#      #  'edition_information':	sd['edition_information'],
#        'publication_year':	    sd['publication_year'],
#      #  'url':	                sd['url'],
#        'image_url':	        sd['image_url'],
#        'book_id':	            sd['book_id'],
#        'ratings_count':	    sd['ratings_count'],
#       # 'work_id':	            sd['work_id'],
#        'title':	            sd['title']
#       # 'title_without_series':	sd['title_without_series']
#        })
#    return book_data
#
#
