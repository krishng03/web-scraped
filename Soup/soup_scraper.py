from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

BASE_URL = 'https://www.fatsecret.com/calories-nutrition/food/soup'

CALORIES = ''
TOTAL_CARBS = '/carbohydrate'
TOTAL_FATS = '/fat'
PROTEINS = '/protein'
CHOLESTROL = '/cholesterol'
VITAMINS = '/vitamins'
SODIUM = '/sodium'

session = requests.Session()

def get_data(URL):
    response = session.get(BASE_URL + URL)
    SOUP = BeautifulSoup(response.text, 'lxml')
    soup_headings = [heading.text for heading in SOUP.select('table.nutrition thead th.nutrient')]

    i = 0
    soup_table_rows = SOUP.select('table.nutrition tbody tr')
    MAX_LEN = len(soup_table_rows)
    SOUP_DATA = []

    while (i < MAX_LEN):
        soup_table_row = soup_table_rows[i]
        if not soup_table_row.has_attr('class'):
            SOUP_DATA.append({})
        else:
            soup_values = ['0.00' if val.text == '-' else val.text for val in soup_table_row.select('td.nutrient')]
            soup_object = {}
            for key, value in zip(soup_headings, soup_values):
                soup_object[key] = value
            SOUP_DATA.append(soup_object)
        i += 1
    
    return SOUP_DATA

CALORIES_DATA = get_data(CALORIES)

CARBS_DATA = get_data(TOTAL_CARBS)

FATS_DATA = get_data(TOTAL_FATS)

PROTEINS_DATA = get_data(PROTEINS)

CHOLESTROL_DATA = get_data(CHOLESTROL)

VITAMINS_DATA = get_data(VITAMINS)

SODIUMDATA = get_data(SODIUM)


# Storing data'

calories_response = session.get(BASE_URL + CALORIES)
calories_soup = BeautifulSoup(calories_response.text, 'lxml')

i = 0
calories_table_rows = calories_soup.select('table.nutrition tbody tr')
MAX_LEN = len(calories_table_rows)
soup_category = ''
DATA = []

while (i < MAX_LEN):
    soup_table_row = calories_table_rows[i]
    if not soup_table_row.has_attr('class'):
        soup_category = soup_table_row.select_one('h3').find(text=True, recursive=False).strip()
    else:
        soup_name = soup_table_row.select_one('a').text.strip()
        SOUP_PROPERTIES = {
            'Category': soup_category,
            'Name': soup_name
        }
        CALORIES_VALUES = CALORIES_DATA[i]
        CARBS_VALUES = CARBS_DATA[i]
        FATS_VALUES = FATS_DATA[i]
        PROTEINS_VALUES = PROTEINS_DATA[i]
        CHOLESTROL_VALUES = CHOLESTROL_DATA[i]
        VITAMINS_VALUES = VITAMINS_DATA[i]
        SODIUM_VALUES = SODIUMDATA[i]
        data_object = SOUP_PROPERTIES | CALORIES_VALUES | CARBS_VALUES | FATS_VALUES | PROTEINS_VALUES | CHOLESTROL_VALUES | VITAMINS_VALUES | SODIUM_VALUES
        DATA.append(data_object)
    i += 1
    
with open('soup_json.json', 'w') as json_file:
    json.dump(DATA, json_file, indent=2)

print('JSON File Saved Successfully!') 

df = pd.DataFrame(DATA)
df.to_csv('soup.csv', index=False)

print('CSV File Saved Successfully!')