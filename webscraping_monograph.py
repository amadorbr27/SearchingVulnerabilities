import requests
from bs4 import BeautifulSoup
import json
import html2text
from database_creation import dbManager
import csv

ANDROID_VERSIONS = ["1.0", "1.1", "1.5", "1.6", "2.0", "2.1", "2.2", "2.3", "3.0", "3.2", "4.0", "4.1", "4.3", "4.4", "5.0",
                    "5.1", "6.0", "7", "7.0", "7.1", "8", "8.0", "8.1", "9", "10", "11", "12", "13"]

NUMBER_PAGES_TO_SCRAP = 25

DROP_WORDS = ["apple"]

class BypassFRPFilesScraper():
    c_link = ""
    title = ""
    vendor = "Unknown"
    id_vendor = None
    model = []
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
        if filter:
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
        for vendorr in dic:
            for modell in dic[vendorr]:
                if vendorr.lower() in self.title.lower():
                    self.vendor = vendorr
                    if modell.lower() in self.title.lower():
                        self.model.append(modell)
        if not self.model:
            self.model = "Unknown"
        else:
            self.model = max(self.model)

        for version in ANDROID_VERSIONS:
            if ("Android " + version) in self.title:
                self.android_version = version

    def scrapArticle(self):
        soup = self.getSoup(self.url, "entry-content")
        self.contents = soup.find_all(class_="lwptoc_item")
        for i in range(len(self.contents)):
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

if __name__ == '__main__':
    manager = dbManager()
    scraper = BypassFRPFilesScraper("")
    count = 1

    for url in scraper.getArticleLinks(NUMBER_PAGES_TO_SCRAP):
        count += 1
        print("Scraping article " + str(count) + "...")
        
        if not manager.isInDatabase(url):
            scraper = BypassFRPFilesScraper(url)
            scraper.scrapBasicAttributes()
            
            if not any(word.lower() in scraper.title.lower() for word in DROP_WORDS):
                scraper.scrapArticle()
                scraper = manager.getArticleVendorId(scraper)
                scraper = manager.getArticlesModelId(scraper)
                manager.addArticle(scraper)
                manager.addArticlesLinks(scraper)

    with open('collected_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Vendor', 'Model', 'Android Version', 'Publication Date', 'Content'])
        for article in manager.get_all_articles():
            writer.writerow([
                article.title,
                article.vendor,
                article.model,
                article.android_version,
                article.publication_date,
                article.content
            ])


    print('CSV file generated successfully!')
