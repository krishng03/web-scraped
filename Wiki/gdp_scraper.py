from bs4 import BeautifulSoup
import requests
import json

URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

response = requests.get(URL)

soup = BeautifulSoup(response.text, 'lxml')

table_rows = soup.select('table.wikitable tr')

GDP_DATA = []

for row in table_rows[3:]:
    country_name = row.select_one('a').text

    gdp_values = [cell.find(text=True, recursive=False).strip() for cell in row.select('td')[1:]]

    updated_gdp_values = ['NA' if x == '—' else x for x in gdp_values for _ in (range(2) if x == '—' else range(1))]

    GDP_DATA.append({
        'country_name': country_name,
        'imf': {
            'forecast': updated_gdp_values[0],
            'year': updated_gdp_values[1],
        },
        'world_bank': {
            'forecast': updated_gdp_values[2],
            'year': updated_gdp_values[3],
        },
        'united_nations': {
            'forecast': updated_gdp_values[4],
            'year': updated_gdp_values[5],
        },
    })

with open('gdp_data.json', 'w') as file:
    json.dump(GDP_DATA, file, indent=2)

print('JSON file saved successfully')
