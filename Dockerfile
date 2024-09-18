# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar o restante do código
COPY . .

# Definir variável de ambiente para a porta
ENV PORT=8080  # Seguindo a prática recomendada, corrigindo o formato

# Comando de entrada para iniciar o Streamlit
CMD streamlit run front_upload_video_azure.py --server.port $PORT --server.enableCORS false
