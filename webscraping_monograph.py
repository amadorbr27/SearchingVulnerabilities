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

class bypassfrpfilesScraper():
    # *Name could be the same as in database
    c_link = ""
    title = ""
    vendor = "Unknown"
    id_vendor = None
    model = list()
    id_model = None
    android_version = "Unknown"
    publication_date = ""
    contents = []
    links = []
    content = ""

    def __init__(self, url):
        self.url = url
        self.c_link = url


    def getSoup(self, url, filter=None):
        response = requests.get(url).text

        soup = BeautifulSoup(response, 'html.parser')
        if filter != None:
            response = str(soup.find(class_=filter))
            soup = BeautifulSoup(response, 'html.parser')

        return soup

    def excludeSummary(self, soup):
        # Deleting contents for main text
        for div in soup.find_all("div", {'class': 'lwptoc_i'}):
            div.decompose()
        return soup

    def removeImages(self, soup):
        # Removing image links
        while True:
            try:
                soup.img.decompose()
            except:
                break
        return soup

    def summaryListFilter(self, contents):
        # Treating summary of contents
        contentlist = str(list(contents.keys())).replace("'", " ")
        contentlist = "".join(contentlist)
        return contentlist

    def scrapBasicAttributes(self):
        soup = self.getSoup(self.url, "entry-header")
        self.title = soup.find('h1').text
        self.publication_date = soup.find("time")["datetime"]

        # Treating datetime
        self.publication_date = self.publication_date.split("+")[0].replace("T", " ")

        # Filtering vendor and model
        with open("Phones_Models_List.json", "r") as text:
            dic = json.load(text)
        for vendorr in dic:
            for modell in dic[vendorr]:
                if (vendorr.lower() in self.title.lower()):
                    self.vendor = vendorr
                    if (modell.lower() in self.title.lower()):
                        if isinstance(self.model, list):
                            self.model = max(self.model, key=len)
                        else:
                            self.model = modell

        # Filtering android version
        for version in ANDROID_VERSIONS:
            if ("Android " + version) in self.title:
                self.android_version = version


    def scrapArticle(self):
        soup = self.getSoup(self.url, "entry-content")

        # Filtering titles of contents
        # * Format need revision
        self.contents = soup.find_all(class_="lwptoc_item")
        for i in range(0, len(self.contents)):
            self.contents[i] = self.contents[i].text.split()
            self.contents[i] = " ".join(self.contents[i])
        self.contents = dict.fromkeys(self.contents)

        soup = self.excludeSummary(soup)

        # Filtering related links
        href_tags = soup.find_all(href=True)
        for tag in href_tags:
            self.links.append(tag['href'])

        soup = self.removeImages(soup)

        # Filtering text content
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
    article = bypassfrpfilesScraper("")
    count = 1
    scraped_data = []

    for url in article.getArticleLinks(NUMBER_PAGES_TO_SCRAP):
        count += 1
        print("Scraping article " + str(count) + "...")
        if not manager.isInDatabase(url):
            # Declaring scraper instance and making the web scraping
            article = bypassfrpfilesScraper(url)
            article.scrapBasicAttributes()

            # Dropping articles with drop words
            if not any(word.lower() in article.title.lower() for word in DROP_WORDS):
                article.scrapArticle()

                # Search and set vendor and model
                article = manager.getArticleVendorId(article)
                article = manager.getArticlesModelId(article)

                manager.addArticle(article)

                # Adding relation data into articles_links table
                manager.addArticlesLinks(article)

                scraped_data.append({
                    'title': article.title,
                    'vendor': article.vendor,
                    'model': article.model,
                    'android_version': article.android_version,
                    'publication_date': article.publication_date,
                    'content': article.content
                })

    return jsonify(scraped_data)

if __name__ == '__main__':
    app.run()
