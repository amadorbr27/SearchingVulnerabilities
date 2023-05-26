import requests
from bs4 import BeautifulSoup
import json
import html2text
import mysql.connector as mysql
from database_creation import dbManager
from flask import Flask, jsonify

ANDROID_VERSIONS = ["1.0", "1.1", "1.5", "1.6", "2.0", "2.1", "2.2", "2.3", "3.0", "3.2", "4.0", "4.1", "4.3", "4.4", "5.0",
                    "5.1", "6.0", "7", "7.0", "7.1", "8", "8.0", "8.1", "9", "10", "11", "12", "13"]

NUMBER_PAGES_TO_SCRAP = 25

DROP_WORDS = ["apple"]

app = Flask(__name__)

class BypassfrpfilesScraper:
    def __init__(self, url):
        self.url = url
        self.c_link = url
        self.title = ""
        self.vendor = "Unknown"
        self.id_vendor = None
        self.model = []
        self.id_model = None
        self.android_version = "Unknown"
        self.publication_date = ""
        self.contents = []
        self.links = []
        self.content = ""

    def getSoup(self, url, filter=None):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        if filter is not None:
            response = str(soup.find(class_=filter))
            soup = BeautifulSoup(response, 'html.parser')
        return soup

    def excludeSummary(self, soup):
        for div in soup.find_all("div", {'class': 'lwptoc_i'}):
            div.decompose()
        return soup

    def removeImages(self, soup):
        while True:
            try:
                soup.img.decompose()
            except:
                break
        return soup

    def summaryListFilter(self, contents):
        contentlist = str(list(contents.keys())).replace("'", " ")
        contentlist = "".join(contentlist)
        return contentlist

    def scrapBasicAttributes(self):
        soup = self.getSoup(self.url, "entry-header")
        self.title = soup.find('h1').text
        self.publication_date = soup.find("time")["datetime"]
        self.publication_date = self.publication_date.split("+")[0].replace("T", " ")

        with open("Phones_Models_List.json", "r") as text:
            dic = json.load(text)
        for vendor in dic:
            for model in dic[vendor]:
                if vendor.lower() in self.title.lower():
                    self.vendor = vendor
                    if model.lower() in self.title.lower():
                        if isinstance(self.model, list):
                            self.model = max(self.model, key=len)
                        else:
                            self.model = model

        for version in ANDROID_VERSIONS:
            if f"Android {version}" in self.title:
                self.android_version = version

    def scrapArticle(self):
        soup = self.getSoup(self.url, "entry-content")
        self.contents = soup.find_all(class_="lwptoc_item")
        for i in range(0, len(self.contents)):
            self.contents[i] = " ".join(self.contents[i].text.split())
        self.contents = dict.fromkeys(self.contents)

        soup = self.excludeSummary(soup)
        href_tags = soup.find_all(href=True)
        for tag in href_tags:
            self.links.append(tag['href'])

        soup = self.removeImages(soup)
        self.content = html2text.html2text(str(soup))

    def getArticleLinks(self, npages):
        urls = []
        for n in range(1, npages):
            url = f"https://www.bypassfrpfiles.com/page/{n}/"
            soup = self.getSoup(url)
            results = soup.find_all(class_="entry-title")
            for result in results:
                href_tag = result.find(href=True)
                urls.append(href_tag['href'])
        return urls

@app.route('/')
def scrape_and_return_data():
    manager = dbManager()
    article_scraper = BypassfrpfilesScraper("")
    count = 1
    scraped_data = []

    for url in article_scraper.getArticleLinks(NUMBER_PAGES_TO_SCRAP):
        count += 1
        print("Scraping article " + str(count) + "...")
        if not manager.isInDatabase(url):
            article_scraper = BypassfrpfilesScraper(url)
            article_scraper.scrapBasicAttributes()

            if not any(word.lower() in article_scraper.title.lower() for word in DROP_WORDS):
                article_scraper.scrapArticle()
                article_scraper = manager.getArticleVendorId(article_scraper)
                article_scraper = manager.getArticlesModelId(article_scraper)
                manager.addArticle(article_scraper)
                manager.addArticlesLinks(article_scraper)

                scraped_data.append({
                    'title': article_scraper.title,
                    'vendor': article_scraper.vendor,
                    'model': article_scraper.model,
                    'android_version': article_scraper.android_version,
                    'publication_date': article_scraper.publication_date,
                    'content': article_scraper.content
                })

    return jsonify(scraped_data)

if __name__ == '__main__':
    app.run()
