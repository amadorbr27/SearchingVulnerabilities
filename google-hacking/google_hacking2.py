import requests
from bs4 import BeautifulSoup

# Consulta de pesquisa no Google
query = 'site:tudocelular.com cellphones_list'

# Construir a URL da pesquisa no Google
url = f'https://www.google.com/search?q={query}'

# Configurar o User-Agent para evitar bloqueio
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Enviar solicitação HTTP para obter a página de resultados do Google
response = requests.get(url, headers=headers)

# Analisar o HTML da página de resultados do Google
soup = BeautifulSoup(response.text, 'html.parser')

# Extrair os títulos e URLs dos resultados de pesquisa
search_results = soup.find_all('div', class_='yuRUbf')
for result in search_results:
    title = result.find('h3').text
    url = result.find('a')['href']
    print(f'Título: {title}')
    print(f'URL: {url}\n')