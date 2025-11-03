import pandas as pd
import requests
import time
import logging
from tqdm import tqdm

API_KEY = 'cc5834d6192d4d07b69e008e18ff7a1d'
BASE_URL = 'https://api.spoonacular.com/recipes'

SEARCH_REQUESTS = [
    {'cuisine': 'Italian', 'number': 10},
    # {'cuisine': 'Asian', 'number': 80},
    # {'cuisine': 'Mexican', 'number': 80},
    # {'maxReadyTime': 30, 'number': 80},
    # {'minReadyTime': 60, 'number': 80},
    # {'type': 'main course', 'number': 80},
    # {'diet': 'vegetarian', 'number': 80}
]


def search_recipes(params):
    url = f'{BASE_URL}/complexSearch'
    all_params = {'apiKey': API_KEY, **params}

    response = requests.get(url, params=all_params)
    response.raise_for_status()

    data = response.json()
    results = data.get('results', [])
    logging.info(f"Найдено {len(results)} рецептов для параметров: {params}")

    return results


def get_recipe_details(recipe_id):
    url = f'{BASE_URL}/{recipe_id}/information'
    all_params = {'apiKey': API_KEY}

    response = requests.get(url, params=all_params)
    response.raise_for_status()

    data = response.json()

    data.pop('instructions', None)
    data.pop('analyzedInstructions', None)
    data.pop('image', None)

    logging.info(f"Получены детали рецепта с id={recipe_id}")

    return data


all_recipes = []
used_recipes = set()

for search_params in tqdm(SEARCH_REQUESTS, desc="Обработка запросов"):
    try:
        search_results = search_recipes(search_params)

        for recipe in search_results:
            recipe_id = recipe['id']

            if recipe_id in used_recipes:
                continue

            try:
                recipe_data = get_recipe_details(recipe_id)

                recipe_data.update({
                    'cuisine': ', '.join(recipe_data.get('cuisines', [])),
                    'dishType': ', '.join(recipe_data.get('dishTypes', [])),
                    'veryHealthy': recipe_data.get('veryHealthy', False),
                })

                all_recipes.append(recipe_data)
                used_recipes.add(recipe_id)
                time.sleep(0.5)

            except Exception as exc:
                logging.error(f"Ошибка при получении деталей рецепта {recipe_id}: {exc}")
                continue

    except Exception as exc:
        logging.error(f"Ошибка при поиске с параметрами {search_params}: {exc}")
        continue

df = pd.DataFrame(all_recipes)

filename = 'reciped_and_details.csv'
df.to_csv(filename, index=False, encoding='utf-8')