FROM python:3.11-slim

WORKDIR /phishlab

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 3000

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--timeout", "300", "wsgi:app"]
