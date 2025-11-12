import pandas as pd
import json

with open('result_recipes.json', 'r') as f:
    recipes_data = json.load(f)

recipes_df = pd.DataFrame(recipes_data)
reviews_df = pd.read_csv('reviews_bbc.csv')
merged_data = reviews_df.merge(recipes_df, on='title', how='left')
recipe_review_counts = merged_data.groupby('title').size().reset_index(name='review_count')
merged_data = merged_data.merge(recipe_review_counts, on='title', how='left')
filtered_data = merged_data[merged_data['review_count'] >= 50]
filtered_data = filtered_data.drop('user', axis=1)