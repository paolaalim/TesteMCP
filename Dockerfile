FROM python:3.13.1-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 6277  # Apenas documentação — não ativa o uso de rede se for stdio

CMD ["python", "servidor.py"]
