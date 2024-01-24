FROM python:3.10

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y sqlite3

RUN sqlite3 bank.db < init.sql

CMD ["python", "app.py"]
