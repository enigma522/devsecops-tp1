FROM python:3.7

ENV DB_PASSWORD="supersecret123"

RUN apt-get update && apt-get install -y curl vim

COPY . /app

WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]