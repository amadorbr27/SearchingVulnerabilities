import requests
from bs4 import BeautifulSoup

# Consulta de pesquisa no Google
query = 'android motorola vulnerabilities'

# Construir a URL da pesquisa no Google
url = f'https://www.google.com/search?q={query}'

# Enviar solicitação HTTP para obter a página de resultados do Google
response = requests.get(url)

# Analisar o HTML da página de resultados do Google
soup = BeautifulSoup(response.text, 'html.parser')

# Extrair os links dos resultados da pesquisa
links = soup.find_all('a')

# Imprimir os URLs dos resultados
for link in links:
    print(link.get('href'))
