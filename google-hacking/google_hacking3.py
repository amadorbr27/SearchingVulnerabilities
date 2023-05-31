import requests
from bs4 import BeautifulSoup

# URL do site que contém as informações das marcas de celular
url = 'https://www.gsmarena.com/makers.php3'

# Enviar solicitação HTTP para obter a página de marcas de celular
response = requests.get(url)

# Analisar o HTML da página de marcas de celular
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a div que contém as marcas de celular
brand_div = soup.find('div', class_='st-text')

# Encontrar os elementos <a> dentro da div
brand_links = brand_div.find_all('a')

# Extrair as marcas de celular dos links
for brand_link in brand_links:
    brand = brand_link.text.strip()
    print(f'Marca: {brand}')
