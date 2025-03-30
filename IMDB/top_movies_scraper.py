from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import json

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

BASE_URL = 'https://www.imdb.com'
MOVIES_JSON_FILE = 'movies.json'

session = requests.Session()
session.headers.update(headers)

url = f'{BASE_URL}/chart/top/'
response = session.get(url)

movies_soup = BeautifulSoup(response.text, 'lxml')

movies_tiles = movies_soup.select('li.ipc-metadata-list-summary-item')
MOVIES_COUNT = len(movies_tiles)
movies_info = []
iter = 1

for i, movie in enumerate(movies_tiles, start=1):
    try:
        movie_name = movie.select_one('h3.ipc-title__text').text.split('.')[1][1:]
        movie_data = [span.text for span in movie.select('span.cli-title-metadata-item')]
        movie_imdb_rating = movie.select_one('span.ipc-rating-star--rating').text
        movie_imdb_vote_count = movie.select_one('span.ipc-rating-star--voteCount').text.split('(')[1][:-1]

        movie_href = movie.select_one('a.ipc-title-link-wrapper')['href']

        tags_response = session.get(f'{BASE_URL}{movie_href}')

        tags_soup = BeautifulSoup(tags_response.text, 'lxml')

        movie_tags = [tag.text for tag in tags_soup.select('div.ipc-chip-list__scroller span.ipc-chip__text')]
        movies_info.append({
            'movie_name': movie_name,
            'movie_release_year': movie_data[0],
            'movie_duration': movie_data[1],
            'movie_rating': movie_data[2],
            'movie_imdb_rating': movie_imdb_rating,
            'movie_imdb_vote_count': movie_imdb_vote_count,
            'movie_tags': movie_tags
        })
        
        print(f'Iteration done ({i}/{MOVIES_COUNT})')
    
    except Exception as e:
        print(f'Error Ocurred: {e}')

with open(MOVIES_JSON_FILE, 'w') as movies_file:
    json.dump(movies_info, movies_file, indent=2)

print(f'JSON file saved successfully at : {MOVIES_JSON_FILE}')
