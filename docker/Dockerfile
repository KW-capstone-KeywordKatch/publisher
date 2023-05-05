# base image
FROM node:latest AS build

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential

WORKDIR /app/keywordkatch/client

COPY client/package*.json ./

RUN npm install;
RUN npm upgrade;
RUN npm update;

COPY client/ ./

RUN npm run build;

RUN ls;

FROM python:latest As Server

WORKDIR /app/keywordkatch/python

COPY python/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY python/ ./

RUN ls;

WORKDIR /app/keywordkatch

COPY --from=build /app/keywordkatch/client /app/keywordkatch/client

RUN ls;

WORKDIR /app/keywordkatch/python

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# start the Flask application
CMD ["python3","main.py"]