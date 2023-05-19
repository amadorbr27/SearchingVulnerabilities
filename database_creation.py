import mysql.connector
import json
from dotenv import load_dotenv
from dotenv import dotenv_values


class dbManager:
    def __init__(self):
        # Load environment variables from a .env file
        load_dotenv()
        
        # Load configuration values from the .env file
        config = dotenv_values(".env")

       # Establish a database connection
        self.db = mysql.connector.connect(
            host = config["DB_HOST"],
            port = config["DB_PORT"],
            user = config["DB_USER"],
            password = config["DB_PASSWORD"],
            database = config['DB_NAME']

        )

        self.cursor = self.db.cursor()

        statements = [
             
            "DROP TABLE IF EXISTS `article_links`;",
            "DROP TABLE IF EXISTS `articles`;",
            "DROP TABLE IF EXISTS `links`;",
            "DROP TABLE IF EXISTS `models`;",
            "DROP TABLE IF EXISTS `vendors`;",
            "CREATE TABLE `vendors` ("
            " `id` int NOT NULL AUTO_INCREMENT,"
            " `c_vendor` varchar(45) NOT NULL,"
            " PRIMARY KEY (`id`),"
            " UNIQUE KEY `id_UNIQUE` (`id`),"
            " UNIQUE KEY `c_vendor_UNIQUE` (`c_vendor`))"
            ,
            "CREATE TABLE `models` ("
            " `id` int NOT NULL AUTO_INCREMENT, "
            " `c_model` varchar(45) NOT NULL, "
            " `id_vendor` int DEFAULT NULL, "
            " PRIMARY KEY(`id`), "
            " UNIQUE KEY `id_UNIQUE` (`id`), "
            " KEY `id_vendor_idx` (`id_vendor`), "
            " CONSTRAINT `id_vendor` FOREIGN KEY (`id_vendor`) REFERENCES `vendors` (`id`))"
            ,
            "INSERT INTO models (id, c_model, id_vendor) VALUES (1, 'Unknown', NULL)",
            "CREATE TABLE `links` ("
            "  `id` int NOT NULL AUTO_INCREMENT,"
            "  `c_link` varchar(450) NOT NULL,"
            "  PRIMARY KEY (`id`),"
            "  UNIQUE KEY `id_UNIQUE` (`id`),"
            "  UNIQUE KEY `c_link_UNIQUE` (`c_link`))"
            ,
            "CREATE TABLE `articles` ("
            "  `id` int NOT NULL AUTO_INCREMENT,"
            "  `id_model` int DEFAULT NULL,"
            "  `c_title` varchar(450) NOT NULL,"
            "  `n_android_version` float DEFAULT NULL,"
            "  `d_publication` datetime DEFAULT NULL,"
            "  `c_link` varchar(450) NOT NULL,"
            "  `c_summary` varchar(450) DEFAULT NULL,"
            "  `c_markdown_contents` text,"
            "  `c_json_contents` json DEFAULT NULL,"
            "  PRIMARY KEY (`id`),"
            "  UNIQUE KEY `id_UNIQUE` (`id`),"
            "  UNIQUE KEY `d_publication_UNIQUE` (`d_publication`),"
            "  UNIQUE KEY `c_link_UNIQUE` (`c_link`),"
            "  KEY `id_model_idx` (`id_model`),"
            "  CONSTRAINT `id_model` FOREIGN KEY (`id_model`) REFERENCES `models` (`id`))"
            ,

            (
                "CREATE TABLE `articles_links` ("
                "  `id_article` INT NOT NULL,"
                "  `id_link` INT NOT NULL,"
                "  PRIMARY KEY (`id_article`, `id_link`),"
                "  CONSTRAINT `id_article`"
                "    FOREIGN KEY (`id_article`)"
                "    REFERENCES `articles` (`id`)"
                "    ON DELETE NO ACTION"
                "    ON UPDATE NO ACTION,"
                "  CONSTRAINT `id_link`"
                "    FOREIGN KEY (`id_link`)"
                "    REFERENCES `links` (`id`))"
            ),
        ]
        
        #create or reacreate database structure if already exist, earising all data
        for statament in statements:
            self.cursor.execute(statament)

    def createTables(self):
        # Show tables that were created
        self.cursor.execute("SHOW TABLES")
        print(self.cursor.fetchall())


    #the isInDatabase method checks if a certain URL (url) already exists in the articles table of the database.
    def isInDatabase(self, url):
        self.cursor.execute(f"SELECT c_link FROM articles WHERE c_link = '{url}'")
        result = self.cursor.fetchall()

        if len(result) == 0:
            return False
        else:
            return True
        
    #Querying the article in the database by id
    def selectArticleId(self, article):
        self.cursor.execute(f"SELECT id FROM articles WHERE c_link ='{article.c_link}'")
        result = self.cursor.fetchall()
        return result[0][0]
    
    #Consulting all links and Inserting new links
    def addArticle(self, article):
        
        # Collecting and saving the model ID
        
        self.cursor.execute(f"SELECT id FROM articles WHERE c_link = '{article.c_link}'")
        result = self.cursor.fetchall()

        if len(result) == 0:
            #if the article does not exist, insert it into the 'articles' table
            query = "INSERT INTO articles (c_title, d_publication, c_link, c_summary, c_markdown_contents) VALUES (%s, %s, %s, %s, %s)"
            values = (article.title, article.publication_date, article.c_link, article.summaryListFilter(article.contents), article.content)
            self.cursor.execute(query, values)
            self.db.commit()

        id_article = self.selectArticleId(article)
        
        # Updating model
        if article.model != "Unknown":
            self.cursor.execute(f"SELECT id FROM models WHERE c_model = '{article.model}'")
            result = self.cursor.fetchall()
            if len(result) == 0:
                print("Novo modelo detectado, atualize o banco de dados.")
            else:
                self.cursor.execute(f"UPDATE articles SET id_model = '{result[0][0]}' WHERE id = '{id_article}'")
                self.db.commit()

        # Updating android version
        if article.android_version != "Unknown":
            self.cursor.execute(
                f"UPDATE articles SET n_android_version = '{article.android_version}' WHERE id = '{id_article}'"
            )
            self.db.commit()

    
    def addArticlesLinks(self, article):
        id_article = self.selectArticleId(article)
        for link in article.links:
            self.cursor.execute(f"SELECT id FROM links WHERE c_link = '{link}'")
            result = self.cursor.fetchall()
            if len(result) != 0:
                # * due one query or use another way
                self.cursor.execute(f"SELECT id_article, id_link FROM articles_links WHERE id_article = '{id_article}'")
                result2 = self.cursor.fetchall()
                self.cursor.execute(f"SELECT id_article, id_link FROM articles_links WHERE id_link = '{result[0][0]}'")
                result3 = self.cursor.fetchall()
                if (result2 in result3) or (result3 in result2):
                    self.cursor.execute(
                        f"INSERT INTO articles_links (id_article, id_link) VALUES ('{id_article}', '{result[0][0]}')")
                    self.db.commit()


    def getArticleVendorId(self, article):
        """
        :param article: article to find vendor or add to database
        :return: article with id_vendor
        """
        self.cursor.execute(f"SELECT id FROM vendors WHERE c_vendor = '{article.vendor}'")
        result = self.cursor.fetchall()

        if len(result) == 0:
            self.cursor.execute(f"INSERT INTO vendors (c_vendor) VALUES ('{article.vendor}')")
            self.db.commit()
            self.cursor.execute(f"SELECT id FROM vendors WHERE c_vendor = '{article.vendor}'")
            id_vendor = self.cursor.fetchall()[0][0]
        else:
            id_vendor = result[0][0]

        article.id_vendor = id_vendor
        return article
    

    def addVendors(self, article):
        """
        :param article: article to add vendors
        :return:
        """
        vendor_id = self.getArticleVendorId(article)
        self.cursor.execute(f"SELECT id_article FROM articles WHERE c_link = '{article.c_link}'")
        result = self.cursor.fetchall()
        id_article = result[0][0]
        self.cursor.execute(
            f"INSERT INTO articles_vendors (id_article, id_vendor) VALUES ('{id_article}', '{vendor_id}')"
        )
        self.db.commit()
    
    def getArticlesModelId(self, article):
        """
        :param article: article to find model  or add to database
        :return: article with id_model
        """
        id_model = None
        self.cursor.execute(f"SELECT id FROM models WHERE c_model = '{article.model}' AND id_vendor = {article.id_vendor}")
        result = self.cursor.fetchall()

        if len(result)==0:
            self.cursor.execute(f"INSERT INTO models (c_model, id_vendor ) VALUES ('{article.model}', {article.id_vendor})")
            self.db.commit()
            self.cursor.execute(f"SELECT id FROM models WHERE c_model = '{article.model}' AND id_vendor = {article.id_vendor}")
            id_model = self.cursor.fetchall()[0][0]
        else:
            id_model = result[0][0]

        article.id_model = id_model
        return article

if __name__ == '__main__':
    # Create an instance of the dbManager class
    manager = dbManager()

    # Create tables in the database
    manager.createTables()
