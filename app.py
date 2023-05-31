from flask import Flask, render_template, jsonify, request
from smartphones_models_scraping import modelScraping
import mysql.connector as mysql
import json
import math
import markdown
import subprocess
from decouple import config

ITEMS_PER_PAGE = 20

class App:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = mysql.connect(
            host=config('DB_HOST'),
            port=config('DB_PORT'),
            user=config('DB_USER'),
            passwd=config('DB_PASSWORD'),
            database=config('DB_DATABASE')
        )
        self.cursor = self.db.cursor()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app_obj = App()  # Criar uma instância única da classe App

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/article_example")
def example():
    return render_template("article_example.html")

@app.route('/get_new_models')
def get_new_models():
    new_models_formated = ""
    # Load the dictionary from the JSON file
    with open("Phones_Models_List.json", "r") as text:
        dic = json.load(text)

    x = modelScraping()
    dic = x.updateModels(dic=dic)

    i = 0
    for model in x.new_models:
        i = i + 1
        # String to be shown in HTML after update
        new_models_formated += f"{i} - {model} <br> "

    # Ensure no duplicated models
    for key in dic.keys():
        dic[key] = list(dict.fromkeys(dic[key]))

    # Write the updated dictionary back to the JSON file
    with open("Phones_Models_List.json", "w") as text:
        json.dump(dic, text, indent=4)

    return jsonify(new_models_formated)

@app.route('/bypassfrpfiles', methods=['POST', 'GET'])
def bypassfrpfiles():
    app_obj.connect()

    query = "SELECT * FROM articles ORDER BY d_publication DESC"
    app_obj.cursor.execute(query)
    articles = app_obj.cursor.fetchall()

    # Calculate the total number of pages
    total_items = len(articles)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)

    # Get the current page number
    page = int(request.args.get('page', 1))

    # Determine the start and end indices of the items for the current page
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    # Slice the articles list to only include the items for the current page
    current_page_articles = articles[start:end]

    current_page = request.args.get('page')
    if not current_page:
        current_page = 1

    return render_template('bypassfrpfiles_listed.html', data=current_page_articles, page=page, total_pages=total_pages, current_page=current_page)

@app.route('/show_article/<int:article_id>')
def show_article(article_id):
    app_obj.connect()

    # Retrieve the tuple item using the article_id
    app_obj.cursor.execute(f"SELECT * FROM articles WHERE id = {article_id}")
    article = app_obj.cursor.fetchone()

    # Convert markdown content to HTML
    article = list(article)
    app_obj.cursor.execute(f"SELECT c_model, id_vendor FROM models WHERE id = '{article[1]}'")
    result = app_obj.cursor.fetchall()

    if len(result) != 0:
        article[1] = result[0][0]
        app_obj.cursor.execute(f"SELECT c_vendor FROM vendors WHERE id = {result[0][1]}")
        result = app_obj.cursor.fetchall()
        article[0] = result[0][0]
    else:
        article[1] = "Unknown"
        article[0] = "Unknown"

    article[7] = markdown.markdown(article[7]).replace("</h2>", "</h2><br><br>")

    return render_template('show_article.html', article=article)

@app.route('/update_articles')
def update():
    subprocess.run(["python", "webscraping_monograph.py"])

    return bypassfrpfiles()

if __name__ == '__main__':
    app.run(debug=True)
