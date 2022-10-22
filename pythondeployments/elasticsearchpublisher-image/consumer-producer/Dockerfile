FROM python:3.6-buster

RUN apt-get update \
    && apt-get -yy install libmariadb-dev

WORKDIR /app
COPY app/. .

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "-u", "./ElasticSearchPublisherLogic.py" ]