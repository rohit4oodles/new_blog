FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install dj-database-url

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main.wsgi:application"]

