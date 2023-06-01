import requests
from bs4 import BeautifulSoup
import re
import json
import csv

class modelScraping:

    new_models = []

    def getModels(self, number_page):
        dic = {}
        print("number_page =", number_page)

        page = requests.get(f'https://www.tudocelular.com/celulares/fichas-tecnicas_{number_page}.html')

        soup = BeautifulSoup(page.text, 'html.parser')

        #Collecting info from the classes and tags of interest
        models_list = soup.find(id='cellphones_list')
        models_list_items = models_list.find_all('h4')

        #Cleaning and saving in a dictionary, with the vendors as keys
        for model in models_list_items:
            vendor = str(model.contents[0])
            vendor = re.split('strong>|</', vendor)
            fb = vendor[1]

            md = model.contents[1]

            if fb in dic:
                dic[fb].append(md)
            else:
                dic[fb] = [md]

        return dic

    def saveNewModels(self, dic, dic_to_put):
        # Saving the products in dictionary
        # *The count variable is to ignore the first element of the list, because the last item is repeated in the next
        # page list. The method to treat this needs to be revised
        count = 0
        for fb in dic_to_put.keys():
            count = count + 1
            for md in dic_to_put[fb]:
                md = self.treatObss(md)
                if fb in dic:
                    for mod in dic[fb]:
                        # Models may have the same initial name
                        if re.match(f"^{md}$", mod) and count != 1:
                            # return -1 if the model is already in the dataset
                            return dic, -1
                    else:
                        dic[fb].append(md)
                else:
                    dic[fb] = [md]

        return dic, 1

    def updateModels(self, dic):
        control = 0
        i = 1

        while control == 0 and i < 90:
            new_models = self.getModels(i)
            for key in new_models:
                for model in new_models[key]:
                    self.new_models.append(f"{key} {model}")
            dic, result = self.saveNewModels(dic, new_models)
            if result == 1:
                i = i + 1
                print("O resultado é:", i)
            else:
                control = 1
        return dic

    def treatObss(self, string):
        if "(" in string:
            string = string.split("(")
            string = string[0]
        if string[-1] == " ":
            string = list(string)
            string.pop(-1)
            string = "".join(string)
        if string[0] == " ":
            string = list(string)
            string.pop(0)
            string = "".join(string)
        return string


if __name__ == '__main__':
    new_models_formated = ""
    # * Need revision to use the database
    with open("Phones_Models_List.json", "r") as text:
        # * Save json file as dictionary. The file exists and is in json format. Need to be revised
        dic = json.loads(text.read())
    with open("Phones_Models_List.json", "w") as text:
        x = modelScraping()
        dic = x.updateModels(dic=dic)
        i = 0
        for model in x.new_models:
            i = i + 1
            # String shown in HTML after update
            new_models_formated += f"{i} - {model} <br> "

        # Assuring not duplicated models
        for key in dic.keys():
            dic[key] = list(dict.fromkeys(dic[key]))
        json_object = json.dumps(dic, indent=4)
        text.write(json_object)

    print(new_models_formated)

    # Generating CSV file
    csv_filename = "data_scraped.csv"
    data = []
    for vendor, models in dic.items():
        for model in models:
            data.append((vendor, model))

    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["vendor", "model"])  # Header
        writer.writerows(data)  # Data

    print(f"Arquivo CSV '{csv_filename}' gerado com sucesso!")
