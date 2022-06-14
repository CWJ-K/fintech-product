FROM continuumio/miniconda3:4.3.27


RUN apt-get update 
RUN mkdir /FinMindProject

COPY . /FintechProject/

WORKDIR /FintechProject/

RUN pip install --upgrade pip
RUN pip install pipenv && pipenv sync
RUN VERSION=RELEASE python genenv.py