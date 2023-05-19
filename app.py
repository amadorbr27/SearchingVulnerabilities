from flask import Flask, render_template, jsonify, request
from smartphones_models_scraping import modelScraping
import mysql.connector as mysql
import json
import math
import markdown
import subprocess

ITEMS_PER_PAGE = 20

db = mysql.connect(
    host="localhost",
    user="motorola", # Put your username here
    passwd="motorola23", # Put your password here
    database="motorola"  # Put here the database name
)
cursor = db.cursor()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/article_example")
def example():
    return render_template("article_example.html")


@app.route('/get_new_models')
def get_new_models():
    new_models_formated = ""
    # * Need revision to use the database
    with open("Phones_Models_List.json", "r") as text:
        # *Save json file as dictionary. The file exist and is in json format. Need to be revised
        dic = json.loads(text.read())
    with open("Phones_Models_List.json", "w") as text:
        x = modelScraping()
        dic = x.updateModels(dic=dic)
        i = 0
        for model in x.new_models:
            i = i + 1
            # String showed in html after update
            new_models_formated += f"{i} - {model} <br> "

        # Assuring not duplicated models
        for key in dic.keys():
            dic[key] = list(dict.fromkeys(dic[key]))
        json_object = json.dumps(dic, indent=4)
        text.write(json_object)

    return jsonify(new_models_formated)


@app.route('/bypassfrpfiles', methods=['POST', 'GET'])
def update():

    query = "SELECT * FROM articles ORDER BY d_publication DESC"
    cursor.execute(query)
    articles = cursor.fetchall()

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
    # Retrieve the tuple item using the article_id
    cursor.execute(f"SELECT * FROM articles WHERE id = {article_id}")
    article = cursor.fetchone()

    # Converting markdown content to html
    article = list(article)

    print("Id do modelo: " + str(article[1]))

    #Getting model and vendor
    cursor.execute(f"SELECT c_model, id_vendor FROM models WHERE id = '{article[1]}'")
    result = cursor.fetchall()
    if len(result)!=0:
        article[1] = result[0][0]
        cursor.execute(f"SELECT c_vendor FROM vendors WHERE id = {result[0][1]}")
        result = cursor.fetchall()
        article[0] = result[0][0]
    else:
        article[1] = "Unknown"
        article[0] = "Unknown"

    #Give space from subtitle with replace()
    article[7] = markdown.markdown(article[7]).replace("</h2>", "</h2><br><br>")

    return render_template('show_article.html', article=article)

@app.route('/update_articles')
def update_articles_table():
    print("The list of articles will be updated now:\n")
    subprocess.run(["python", "webscraping_monograph.py"])
    print("Update finished.")

    return update()


if __name__ == '__main__':
    app.run(debug=True)
