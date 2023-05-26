from flask import Flask, render_template, jsonify, request
from smartphones_models_scraping import modelScraping
import json
import math
import markdown
import subprocess
import mysql.connector
from database_creation import dbManager

ITEMS_PER_PAGE = 20


class App:
    def __init__(self):
        self.app = Flask(__name__)

        self.db = dbManager()
        self.cursor = self.db.cursor

        # Rotas
        self.app.route("/")(self.index)
        self.app.route("/article_example")(self.example)
        self.app.route("/get_new_models")(self.get_new_models)
        self.app.route("/bypassfrpfiles", methods=['POST', 'GET'])(self.update)
        self.app.route("/show_article/<int:article_id>")(self.show_article)
        self.app.route("/update_articles")(self.update_articles_table)

    def run(self):
        self.app.run(debug=True)

    def index(self):

        return render_template("index.html")

    def example(self):
        return render_template("article_example.html")

    def get_new_models(self):
        # * Need revision to use the database
        with open("Phones_Models_List.json", "r") as text:
            # *Save json file as dictionary. The file exists and is in json format. Need to be revised
            dic = json.loads(text.read())

        with open("Phones_Models_List.json", "w") as text:
            x = modelScraping()
            dic = x.updateModels(dic=dic)
            i = 0
            for model in x.new_models:
                i = i + 1
                # String showed in HTML after update
                print(f"{i} - {model} <br>", end="", file=text)

            # Assuring not duplicated models
            for key in dic.keys():
                dic[key] = list(dict.fromkeys(dic[key]))
            json_object = json.dumps(dic, indent=4)
            text.write(json_object)

        self.db.commit()  # Commit the changes to the database

        return jsonify(dic)

    def update(self):
        query = "SELECT * FROM articles ORDER BY d_publication DESC"
        self.cursor.execute(query)
        articles = self.cursor.fetchall()

        # Calculate the total number of pages
        total_items = len(articles)
        total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

        # Get the current page number from the request
        page = int(request.args.get('page', 1))

        # Determine the start and end indices of the items for the current page
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        # Slice the articles list to only include the items for the current page
        current_page_articles = articles[start:end]

        return render_template('bypassfrpfiles_listed.html', data=current_page_articles, page=page,
                               total_pages=total_pages)

    def show_article(self, article_id):
        # Retrieve the tuple item using the article_id
        self.cursor.execute(f"SELECT * FROM articles WHERE id = {article_id}")
        article = self.cursor.fetchone()

        # Converting markdown content to HTML
        article = list(article)

        # Getting model and vendor
        self.cursor.execute(f"SELECT c_model, id_vendor FROM models WHERE id = '{article[1]}'")
        result = self.cursor.fetchall()
        if len(result) != 0:
            article[1] = result[0][0]
            self.cursor.execute(f"SELECT c_vendor FROM vendors WHERE id = {result[0][1]}")
            result = self.cursor.fetchall()
            article[0] = result[0][0]
        else:
            article[1] = "Unknown"
            article[0] = "Unknown"

        # Give space from subtitle with replace()
        article[7] = markdown.markdown(article[7]).replace("</h2>", "</h2><br><br>")

        return render_template('show_article.html', article=article)

    def update_articles_table(self):
        print("The list of articles will be updated now:\n")
        subprocess.run(["python", "webscraping_monograph.py"])
        print("Update finished.")

        return self.update()


if __name__ == '__main__':
    app = App()
    app.run()