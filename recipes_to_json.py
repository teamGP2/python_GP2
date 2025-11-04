import json

with open('data.json', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)
result_recipes = []
for recipe in data_dict:
    result_recipes.append(
        {
            'id': recipe.get('id'),
            'title': recipe.get('title'),
            'readyInMinutes': recipe.get('readyInMinutes'),
            'vegetarian': recipe.get('vegetarian'),
            'veryPopular': recipe.get('veryPopular'),
            'healthScore': recipe.get('healthScore'),
            'pricePerServing': recipe.get('pricePerServing'),
            'ingredients': [ingr.get('name') for ingr in recipe.get('extendedIngredients')],
        }
    )

with open('result_recipes.json', 'w', encoding='utf-8') as file:
    json.dump(result_recipes, file, ensure_ascii=False, indent=4)