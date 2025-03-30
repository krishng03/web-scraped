from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

PAGE = 1
PAGE_LIMIT = 5
QUOTES_DATA = []

while PAGE <= PAGE_LIMIT:

    url = f'https://quotes.toscrape.com/page/{PAGE}/'

    response = requests.get(url)

    quote_soup = BeautifulSoup(response.text, 'lxml')

    quotes_div = quote_soup.select('div.quote')

    for quote in quotes_div:
        text = quote.select_one("span.text").text[1:-1]

        author_name = quote.select_one('small.author').text
        
        tags = [tag.text for tag in quote.select('a.tag')]

        author_href = quote.select_one('a')['href']
        
        author_page = requests.get(f"https://quotes.toscrape.com/{author_href}/")

        author_soup = BeautifulSoup(author_page.text, 'lxml')

        author_dob = author_soup.select_one('span.author-born-date').text

        author_location = author_soup.select_one('span.author-born-location').text[3:]

        QUOTES_DATA.append({
            'quote': text,
            'author' : {
                'author_name' : author_name,
                'author_dob': author_dob,
                'author_birth_place': author_location,
            },
            'tags': tags,  
        })
    print(f'{PAGE} loop done')
    PAGE += 1

df = pd.DataFrame(QUOTES_DATA)

df.to_csv('Quotes/quotes.csv', index=False)

print('CSV file stored data successfully')

with open('Quotes/quotes.json', 'w') as json_file:
    json.dump(QUOTES_DATA, json_file, indent=2)

print('JSON file stored successfully')