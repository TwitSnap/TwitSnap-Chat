FROM python:3.13.0rc2-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

EXPOSE $PORT

CMD ["python3", "main.py"]
