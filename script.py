import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def fetch_news():
    url = "https://cryptonews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    for item in soup.find_all('div', class_='cn-tile article'):
        title = item.find('h4').text.strip()
        link = item.find('a')['href']
        articles.append({'title': title, 'link': link})

    return articles

def generate_post(title, link):
    content = f"""
---
title: "{title}"
date: {datetime.now().isoformat()}
draft: false
---

Read more at [Cryptonews]({link}).
"""
    return content

news = fetch_news()

if not os.path.exists("content/posts"):
    os.makedirs("content/posts")

for article in news:
    file_name = f"content/posts/{article['title'].replace(' ', '_')}.md"
    with open(file_name, 'w') as file:
        file.write(generate_post(article['title'], article['link']))

os.system("git add .")
os.system("git commit -m 'Update news content'")
os.system("git push origin main")
