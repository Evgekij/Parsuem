import requests
from bs4 import BeautifulSoup as bs
import json


url = "https://sputnik.by/20231030/" #Делаем запрос страницы

headers = {
    "Accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text


with open("index.html", "w", encoding="utf-8") as file: #Сохраням страницу
    file.write(src) 

with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = bs(src, features="html.parser")
all_news = soup.find_all(class_="list__title") #Собираем новости со страницы

project_urls = {}
for item in all_news: #Создаем цикл и собираем заголовки новостей и ссылки на них
    item_href = "https://sputnik.by/" + item.get("href")
    item_text = item.text


    project_urls[item_text] = item_href


for news_name, news_href in project_urls.items():
    rep = ["\"", ":"] #Заменяем символы для правильной работы кода
    for item in rep:
        if item in news_name:
            news_name = news_name.replace(item, "'",)

    req = requests.get(url=news_href, headers=headers)
    src = req.text

    with open(f"data/{news_name}.html", "w", encoding="utf-8") as file:#Cоздаем отдельню папку для страниц, задаем им название
        file.write(src)

    with open(f"data/{news_name}.html", encoding="utf-8") as file:
        src = file.read()


    soup = bs(src, features="html.parser")
    text_st = soup.find("div", class_="article__body").text
    

    with open(f"papers/{news_name}.json", "w", encoding="utf-8") as file:#Сохраняем статьи в отдельные файлы
        json.dump(text_st, file, indent=4, ensure_ascii=False)

