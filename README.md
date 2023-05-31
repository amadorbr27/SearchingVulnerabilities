# **Instalação de Dependências para a Aplicação Python**


Este documento descreve os passos de instalação das dependências necessárias para execução da aplicação que exige as seguintes bibliotecas:

- MySQL Server
- BeautifulSoup
- datetime
- flask
- html2text
- json
- markdown
- mysql.connector
- re
- requests
- subprocess

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

###Instalação do MySQL Server no Windows:

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

Este comando irá instalar as bibliotecas mysql-connector-python, json, requests, beautifulsoup4, html2text, markdown e flask.
