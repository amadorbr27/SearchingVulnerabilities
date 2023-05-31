from googlesearch import search

# Termo de pesquisa para modelos de celulares
query = 'site:gsmarena.com intitle:"Specifications" "Android"'

# Número máximo de resultados a serem retornados
num_results = 5

# Realizar a pesquisa usando Google Hacking
for result in search(query, num_results=num_results):
    print(result)
