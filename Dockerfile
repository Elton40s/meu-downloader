FROM python:3.11-slim

# Instala o ffmpeg no sistema Linux do servidor
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY app.py .
COPY index.html .

# Expõe a porta padrão
EXPOSE 8000

# Inicia o servidor uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]