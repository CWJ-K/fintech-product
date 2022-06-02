FROM continuumio/miniconda3:4.3.27

RUN apt-get update 
RUN mkdir /FinMindProject

COPY . /FinMindProject/

WORKDIR /FinMindProject/


RUN pip install --upgrade pip && pip install pipenv && pipenv sync
RUN VERSION=RELEASE python genenv.py

