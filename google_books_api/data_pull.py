import os 
import requests
# from dotenv import load_dotenv
# load_dotenv()
# API_KEY = os.getenv("API_KEY")
import pandas as pd


##Importing Utils Functions
from utils import pull_from_google_books
from utils import titles_l # Input data
from utils import authors_l # Input data

# Final Books DF
final_books_df = pd.DataFrame()

for title, author in zip(titles_l, authors_l):

    search_term = title
    author = author
    relevance = 'relevance'

    url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}+inauthor{author}&maxResults=1&orderBy={relevance}"
    book_data = pull_from_google_books(url)

    final_books_df = final_books_df.append(book_data)

final_books_df['full_title'] = final_books_df['title'] + " " +final_books_df['subtitle']
print(final_books_df)
## use fuzzy wuzzy... the fuzz...? to get a score how close the two are
## Validation... removing books that don't have the right author
