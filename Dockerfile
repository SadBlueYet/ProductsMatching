FROM python:3.11-slim

RUN mkdir /products_app
WORKDIR /products_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
RUN chmod a+x wait-for-it.sh

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh
