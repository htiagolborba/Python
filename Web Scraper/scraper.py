import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_g1():
    url = "https://g1.globo.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news = []

    for article in soup.find_all('div', class_='feed-post-body'):
        title = article.find('a', class_='feed-post-link').text.strip()
        link = article.find('a', class_='feed-post-link')['href']
        news.append({"source": "G1", "title": title, "link": link})

    return news

def scrape_cnn():
    url = "https://edition.cnn.com/world"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news = []

    for article in soup.find_all('h3', class_='cd__headline'):
        title = article.text.strip()
        link = article.find('a')['href']
        full_link = f"https://edition.cnn.com{link}" if not link.startswith('http') else link
        news.append({"source": "CNN", "title": title, "link": full_link})

    return news

def save_to_csv(news, filename="data/news.csv"):
    os.makedirs("data", exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["source", "title", "link"])
        writer.writeheader()
        writer.writerows(news)

def main():
    print("Scraping news from G1...")
    g1_news = scrape_g1()
    print(f"Found {len(g1_news)} articles from G1.")

    print("Scraping news from CNN...")
    cnn_news = scrape_cnn()
    print(f"Found {len(cnn_news)} articles from CNN.")

    all_news = g1_news + cnn_news
    print(f"Saving {len(all_news)} articles to CSV...")
    save_to_csv(all_news)
    print("Done! News saved to 'data/news.csv'.")

if __name__ == "__main__":
    main()
