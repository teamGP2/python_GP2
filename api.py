import pandas as pd
import requests
import time
import logging
from tqdm import tqdm

API_KEY = 'cc5834d6192d4d07b69e008e18ff7a1d'
BASE_URL = 'https://api.spoonacular.com/recipes'
HEADERS = {'x-api-key': API_KEY}
