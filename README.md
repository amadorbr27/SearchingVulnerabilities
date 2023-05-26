

# **Instalação de Dependências para a Aplicação Python**

<p>Este documento descreve os passos de instalação das dependências necessárias para execução da aplicação que exige as seguintes bibliotecas:</p>

- mysql.connector
- json
- flask
- python-dotenv 
- beatifulsoup4
- Markdown


## **1. Instalação do MySQL Server**

###Instalação do MySQL Server em Linux:

1. Abra o terminal e execute o seguinte comando para atualizar a lista de pacotes disponíveis:

`sudo apt-getupdate`

2. Em seguida, execute o comando abaixo para instalar o MySQL Server:

`sudo apt-get install mysql-server`

3. Durante a instalação, você será solicitado a configurar uma senha para o usuário root do MySQL. Digite e confirme uma senha forte e segura.
4. Após a instalação, você pode verificar se o MySQL Server está em execução com o seguinte comando:

`systemctl status mysql`

5. Se o MySQL Server estiver em execução, você deve ver uma mensagem indicando que o serviço está ativo.


##Instalação do MySQL Server no Windows:

1. Baixe o instalador do MySQL Server no site oficial:[https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
2. Execute o arquivo de instalação e siga as instruções na tela. Durante a instalação, você será solicitado a configurar uma senha para o usuário root do MySQL. Digite e confirme uma senha forte e segura.

###Instalação do MySQL Server no macOS:

1. Baixe o instalador do MySQL Server no site oficial:[https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
2. Execute o arquivo de instalação e siga as instruções na tela. Durante a instalação, você será solicitado a configurar uma senha para o usuário root do MySQL. Digite e confirme uma senha forte e segura.

## **2. Instalação do Python**

O primeiro passo é instalar o Python em sua máquina. Acesse o site oficial do Python ([https://www.python.org/downloads/](https://www.python.org/downloads/)) e baixe a versão mais recente para o seu sistema operacional.



## **3. Instalação do Gerenciador de Pacotes pip**

O pip é um gerenciador de pacotes para o Python, que permite instalar e gerenciar bibliotecas externas. Verifique se o pip já está instalado em sua máquina executando o seguinte comando no terminal:

`pip --version`

Se o pip já estiver instalado, você deve ver uma mensagem informando a versão do pip instalada em sua máquina. Se o pip não estiver instalado, acesse a documentação oficial ([https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)) e siga as instruções de instalação.



## **4. Instalação das Bibliotecas Python**

Para instalar as bibliotecas Python necessárias para a aplicação, execute o seguinte comando no terminal:


`pip install mysql-connector-python json requests beautifulsoup4 html2text markdown flask`



## ** 5. EXECUTANDO O CÓDIGO LOCALMENTE 

`python database_creation.py`

`python app.py `



## Consertado no Momento, Projeto TCC

 Com essa estrutura, o código do Flask está encapsulado em uma classe App. Os métodos correspondentes às rotas do Flask são definidos dentro da classe, e as dependências, como a conexão com o banco de dados, são inicializadas no construtor __init__. Você pode adicionar o código adicional necessário em cada método para que a funcionalidade desejada seja executada corretamente.

Certifique-se de revisar o código e atualizar os métodos get_new_models, update, show_article e update_articles_table com a lógica necessária para cada funcionalidade específica.

Nesse código, fiz as seguintes correções:

Movido o método update para dentro da classe App e removido o decorator @app.route duplicado.
Corrigido o decorator @app.route para @self.app.route nas rotas definidas dentro da classe.
Adicionado o self. antes de cursor e self. antes de app nos trechos correspondentes.
Corrigido a indentação e posicionamento do método show_article para dentro da classe App.
Removido a chamada para self.db.commit() no método get_new_models, pois não parece ser necessário nesse momento.
Feitas outras correções menores de formatação e sintaxe.
Lembre-se de revisar e atualizar o código de acordo com suas necessidades específicas.

O código HTML parece estar correto. No entanto, para mostrar a paginação dos artigos, você precisa atualizar o código na parte de baixo do template, onde a paginação é exibida.

`<div class="pagination"></div>`


## Explicação do Arquivo App.py

Vamos revisar brevemente o que cada método faz:

O método index retorna o conteúdo a ser exibido na página inicial. Ele chama a função render_template para renderizar o template "index.html" e retorna o resultado.

O método example retorna o conteúdo do exemplo de artigo. Ele chama a função render_template para renderizar o template "article_example.html" e retorna o resultado.

O método get_new_models lê um arquivo JSON, realiza scraping de modelos de smartphones usando a classe modelScraping, atualiza o conteúdo do arquivo JSON com os novos modelos encontrados, realiza algumas operações no dicionário resultante e, em seguida, retorna o dicionário convertido em JSON usando a função jsonify.

O método update executa uma consulta SQL para obter todos os artigos do banco de dados, calcula o número total de páginas com base na quantidade de artigos, obtém o número da página atual da solicitação, determina os índices de início e fim dos artigos para a página atual, retorna uma resposta renderizando o template "bypassfrpfiles_listed.html" com os dados dos artigos e informações de paginação.

O método show_article recebe um ID de artigo como parâmetro, executa consultas SQL para obter informações do artigo e das tabelas relacionadas (modelos e fornecedores), converte o conteúdo do artigo de markdown para HTML e, em seguida, retorna uma resposta renderizando o template "show_article.html" com os dados do artigo.

O método update_articles_table executa um processo externo (usando subprocess.run) para atualizar a lista de artigos e, em seguida, chama o método update para retornar uma resposta atualizada.
