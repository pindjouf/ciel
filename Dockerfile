FROM python:3.10-alpine
WORKDIR /
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers sqlite
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN touch ciel.db
RUN sqlite3 ciel.db "CREATE TABLE users (username TEXT, password TEXT);"
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
