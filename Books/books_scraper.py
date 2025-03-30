from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL_LEFT = 'https://books.toscrape.com/catalogue/page-'
BASE_URL_RIGHT = '.html'

CSV_FILE_LOCATION = 'books.csv'

session = requests.Session()

PAGE_COUNT = 25
curr_page = 1

BOOKS_DATA = []

while curr_page <= PAGE_COUNT:
    try:
        URL = BASE_URL_LEFT + str(curr_page) + BASE_URL_RIGHT

        response = session.get(URL)

        soup = BeautifulSoup(response.text, 'lxml')

        book_items = soup.select('ol.row li')

        for book in book_items:
            book_name = book.select_one('h3 a').text
            book_price = book.select_one('p.price_color').text[1:]

            BOOKS_DATA.append({
                'book_name': book_name,
                'book_price': book_price
            })
        
        print(f'Iteration completed ({curr_page}/{PAGE_COUNT})')
        
        curr_page += 1
    
    except Exception as e:
        print(f'Error ocurred: {e}')

df = pd.DataFrame(BOOKS_DATA)

df.to_csv(CSV_FILE_LOCATION, index=False)

print(f'CSV file saved successfully : {CSV_FILE_LOCATION}')
