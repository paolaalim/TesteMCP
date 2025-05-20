FROM python:3.13.1-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Expondo a porta 6277 (apenas documentação; não usada em stdio)
EXPOSE 6277

CMD ["python", "servidor.py"]

