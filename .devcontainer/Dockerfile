FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y libpq-dev

# Instalar dependências do projeto
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip install -r requirements.txt

# Definir o diretório de trabalho
WORKDIR /workspace
