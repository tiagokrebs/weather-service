FROM python:3.6

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y memcached

EXPOSE 11211

CMD service memcached start && python weather-cli.py