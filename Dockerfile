# Imagem base
FROM python:3.10

# Define o diretório de trabalho
# WORKDIR /app

# Copia o arquivo requirements
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Expõe a porta em que seu aplicativo Flask está sendo executado (por exemplo, 5000)
EXPOSE 5000

# Define o comando para executar o aplicativo Flask
CMD ["python", "app.py"]
