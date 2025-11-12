import csv
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import psutil

def kill_chrome_processes(): #функция для очистки процев хрома, тк иначе компьютер начинает тупить, сделан через psutil, библиотека для управления процами, синтаксис честно взят из интернета
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name'].lower()
            if 'chrome' in name or 'chromedriver' in name:
                proc.kill() 
        except:
            pass
# Закрываем все процессы хрома перед началом
kill_chrome_processes()
with open('result_recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

with open('reviews_bbc.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'user', 'rating', 'text', 'date'])
    for i, recipe in enumerate(recipes):
        title = recipe['title']
        print(f"{i + 1}/{len(recipes)}. {title}")

        try:
            search_words = " ".join(title.split()[:3]) #ищем рецепт по первым 3 словам, и получаем ссылку
            search_url = f"https://www.allrecipes.com/search?q={quote(search_words)}"
            driver.get(search_url)
            time.sleep(2)

            # Находим ссылку на рецепт, если нет то пишем в файл строку о том что нет такого
            recipe_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/recipe/']")
            if not recipe_links:
                writer.writerow([title, "No user", 0, "No recipe found", "Unknown"])
                continue
            #переход по ссылке
            recipe_url = recipe_links[0].get_attribute('href')
            driver.get(recipe_url)
            time.sleep(3)

            # прокрутка к отзывам, они в рецепте внизу страницы
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            found_reviews = 0
            previous_count = 0
            load_more_attempts = 0

            # загружаем больше отзывов, пока не найдём хотя бы 100(если их больше 100) или пока не нажмем кнопку 5 раз
            while found_reviews < 100 and load_more_attempts < 5:
                try:
                    # Ищем кнопку Load More по разным селекторам
                    load_more_selectors = [
                        ".mm-recipes-ugc-shared-item-card-list__load-more-button",
                        "button[class*='load-more']",
                        "button:contains('Load More')",
                        "button:contains('Load more')",
                        "button:contains('Show More')"
                    ]
                    load_more_found = False
                    for selector in load_more_selectors:
                        try:
                            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                            for button in buttons:
                                if button.is_displayed() and button.is_enabled():
                                    driver.execute_script("arguments[0].click();", button)
                                    print("Нажата кнопка 'Load More'")
                                    time.sleep(3)
                                    load_more_attempts += 1
                                    load_more_found = True
                                    break
                            if load_more_found:
                                break
                        except:
                            continue
                    # Прокручиваем для загрузки новых отзывов после нажатия кнопок
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                    # Парсим текущие отзывы
                    review_cards = driver.find_elements(By.CSS_SELECTOR,".mm-recipes-ugc-shared-item-card--review, [data-feedback-id*='_']")
                    # Если количество отзывов не изменилось, брейкаем
                    if len(review_cards) == previous_count:
                        break
                    previous_count = len(review_cards)
                    # Парсим новые отзывы
                    for card in review_cards:
                        if found_reviews >= 100:
                            break
                        try:
                            # Имя юзера
                            user_elems = card.find_elements(By.CSS_SELECTOR,".mm-recipes-ugc-shared-card-byline__username a")
                            user = user_elems[0].text.strip() if user_elems else f"user_{found_reviews}"
                            # звёзды
                            stars = card.find_elements(By.CSS_SELECTOR,".ugc-shared-icon-star")
                            rating = len(stars)
                            # Дата
                            date_elems = card.find_elements(By.CSS_SELECTOR,".mm-recipes-ugc-shared-card-meta__date")
                            date = date_elems[0].text.strip() if date_elems else "N/A"
                            # Текст отзыва
                            text_elems = card.find_elements(By.CSS_SELECTOR,".mm-recipes-ugc-shared-item-card__text")
                            text = text_elems[0].text.strip() if text_elems else ""
                            if text and len(text) > 10:
                                writer.writerow([title, user, rating, text, date])
                                found_reviews += 1
                                print(f"Отзыв {found_reviews}: {user} - {rating} Звезд")
                        except Exception as e:
                            continue
                except Exception as e:
                    print(f"Ошибка при загрузке отзывов: {e}")
                    break
            print(f"Найдено отзывов: {found_reviews}")

        except Exception as e:
            print(f"   Ошибка: {e}")
            writer.writerow([title, "Error", 0, f"Error: {e}", "Unknown"])
        time.sleep(2)
# Закрываем драйвер и очищаем все процы хрома
try:
    driver.quit()
except:
    pass
kill_chrome_processes()
print("Готово!")
