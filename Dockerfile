# Usa imagem leve do Python
FROM python:3.11-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência (caso tenha)
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# A build pode ser omitida se não houver transpilação. Se houver algum passo, adicione aqui
# RUN algum_comando_de_build (como um script de preparação, se necessário)

# A porta exposta depende do que seu servidor usa (ex: 6274 ou 8000)
EXPOSE 6274

# O comando final será sobrescrito via smithery.yaml
CMD ["python", "servidor.py"]



