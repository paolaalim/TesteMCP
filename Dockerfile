# Use a imagem completa do Python 3.13 para evitar erros de compilação
FROM python:3.13

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o contêiner
COPY . .

# Exponha a porta que o servidor usará
EXPOSE 8080

# Comando para iniciar o servidor, agora apontando para o 'servidor.py'
CMD ["uvicorn", "servidor:mcp.streamable_http_app", "--host", "0.0.0.0", "--port", "8080"]
