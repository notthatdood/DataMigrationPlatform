FROM python:3.10.7-slim-bullseye

WORKDIR /app

COPY app/. .

RUN apt-get update -y
RUN apt-get install -y build-essential

RUN apt-get -yy install libmariadb-dev
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python","-u","./app.py"]