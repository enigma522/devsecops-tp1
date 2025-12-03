FROM python:3.13-slim


RUN apt-get update && apt-get install -y curl vim

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
