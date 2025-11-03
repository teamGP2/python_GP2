import json
import requests
import time
import logging

API_KEY = '50c52457baef420fb16cbc37314e3ba5'
BASE_URL = 'https://api.spoonacular.com/recipes'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_request(url, params):
    api_key = API_KEY
    all_params = {'apiKey': api_key, **params}

    try:
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response.status_code == 402:
            logging.warning("API ключ исчерпан")
        else:
            logging.error(f"HTTP ошибка: {e}")
            raise
    except Exception as e:
        logging.error(f"Ошибка запроса: {e}")
        raise


def search_recipes_complex_italian():
    cuisines = 'Italian'

    params = {
            'cuisine': cuisines,
            'number': 200
    }

    data = make_request(f'{BASE_URL}/complexSearch', params)
    recipes = data.get('results', [])
    logging.info(f"Найдено {len(recipes)} рецептов по итальянской кухни")
    time.sleep(0.5)

    return recipes


def search_recipes_complex_mexican():
    cuisines = 'Mexican'

    params = {
            'cuisine': cuisines,
            'number': 200
    }

    data = make_request(f'{BASE_URL}/complexSearch', params)
    recipes = data.get('results', [])
    logging.info(f"Найдено {len(recipes)} рецептов по мексиканской кухни")
    time.sleep(0.5)

    return recipes


def search_recipes_complex_chinese():
    cuisines = 'Chinese'

    params = {
            'cuisine': cuisines,
            'number': 200
    }

    data = make_request(f'{BASE_URL}/complexSearch', params)
    recipes = data.get('results', [])
    logging.info(f"Найдено {len(recipes)} рецептов по китайской кухни")
    time.sleep(0.5)

    return recipes


def search_recipes_complex_ready_time():
    params = {
        'maxReadyTime': 30,
        'number': 200
    }

    data = make_request(f'{BASE_URL}/complexSearch', params)
    recipes = data.get('results', [])
    logging.info(f"Найдено {len(recipes)} рецептов по времени приготовления")
    time.sleep(0.5)

    return recipes


def search_recipes_by_nutrients():
    params = {
        'maxCalories': 300,
        'number': 200
    }

    data = make_request(f'{BASE_URL}/findByNutrients', params)
    logging.info(f"Найдено {len(data)} рецептов по питательности")
    return data


def search_recipes_by_ingredients():
    params = {
        'ingredients': 'chicken',
        'number': 200
    }

    data = make_request(f'{BASE_URL}/findByIngredients', params)
    logging.info(f"Найдено {len(data)} рецептов по ингредиентам")
    return data


def get_random_recipes():
    params = {
        'number': 300
    }

    data = make_request(f'{BASE_URL}/random', params)
    recipes = data.get('recipes', [])
    logging.info(f"Найдено {len(recipes)} случайных рецептов")
    return recipes


def get_recipe_info_bulk(recipe_ids):
    if not recipe_ids:
        return []

    ids_string = ','.join(map(str, recipe_ids))
    params = {
        'ids': ids_string
    }

    logging.info(f"Запрашиваем детали для {len(recipe_ids)} рецептов одним bulk-запросом")

    data = make_request(f'{BASE_URL}/informationBulk', params)

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



all_recipe_ids = set()

try:
    complex_recipes_italian = search_recipes_complex_italian()
    all_recipe_ids.update(recipe.get('id') for recipe in complex_recipes_italian)

    complex_recipes_mexican = search_recipes_complex_mexican()
    all_recipe_ids.update(recipe.get('id') for recipe in complex_recipes_mexican)

    complex_recipes_chinese = search_recipes_complex_chinese()
    all_recipe_ids.update(recipe.get('id') for recipe in complex_recipes_chinese)

    complex_recipes_ready_time = search_recipes_complex_ready_time()
    all_recipe_ids.update(recipe.get('id') for recipe in complex_recipes_ready_time)

    nutrient_recipes = search_recipes_by_nutrients()
    all_recipe_ids.update(recipe.get('id') for recipe in nutrient_recipes)

    ingredient_recipes = search_recipes_by_ingredients()
    all_recipe_ids.update(recipe.get('id') for recipe in ingredient_recipes)

    random_recipes = get_random_recipes()
    all_recipe_ids.update(recipe.get('id') for recipe in random_recipes)

    all_recipes_details = get_recipe_info_bulk(list(all_recipe_ids))

except Exception as e:
    print(f"Программа остановлена: {e}")