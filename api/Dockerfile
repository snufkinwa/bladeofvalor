FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget tar && \
    wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar && \
    tar xf stockfish-ubuntu-x86-64-avx2.tar && \
    mv stockfish /usr/local/bin/ && \
    chmod +x /usr/local/bin/stockfish && \
    rm stockfish-ubuntu-x86-64-avx2.tar && \
    apt-get remove -y wget tar && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]