import requests
from bs4 import BeautifulSoup as bs
import lxml


url = "https://www.rbc.ru/life/tag/console"

headers = {
    "Accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text


with open("page.html", "w", encoding="utf-8") as file:
    file.write(src) 

with open("page.html", encoding="utf-8") as file:
    src = file.read()

soup = bs(src, "lxml")
all_news = soup.find_all(class_="info-block-title")

project_urls = {}
for item in all_news:
    item_text = item.text
    item_href = "https://www.rbc.ru" + item.get("href")
    


    project_urls[item_text] = item_href


for news_name, news_href in project_urls.items():
    rep = ["\n", ":"]
    for item in rep:
        if item in news_name:
            news_name = news_name.replace(item,".")
    req = requests.get(url=news_href, headers=headers)
    src = req.text
    
    with open(f"data_1/{news_name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"data_1/{news_name}.html", encoding="utf-8") as file:
        src = file.read()


    soup = bs(src, features="lxml")
    text_st = soup.find("div" , class_="page").find_all(class_="paragraph")

    for biba in text_st:
        novost_text = biba.text
        with open(f"papers_1/{news_name}.txt", "a", encoding="utf-8") as file:
            file.write(f"{novost_text}\n") 

