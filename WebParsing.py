import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
START_PAGE = 1
END_PAGE = 50  # можно указать любое количество страниц

data = []

for page in range(START_PAGE, END_PAGE + 1):
    url = BASE_URL.format(page)
    response = requests.get(url)

    # Проверяем, что страница существует
    if response.status_code != 200:
        print(f"Страница {page} не найдена, пропуск...")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()

        data.append({
            "Название": title,
            "Цена": price,
            "Наличие": availability
        })

# Сохраняем в Excel
df = pd.DataFrame(data)
df.to_excel("books.xlsx", index=False)

print(f"Готово! Файл books.xlsx создан. Собрано {len(data)} книг.")
