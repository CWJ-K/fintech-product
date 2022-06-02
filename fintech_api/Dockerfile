FROM continuumio/miniconda3:4.3.27

RUN apt-get update
RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/

RUN pip install pipenv==2020.6.2 && pipenv sync


RUN VERSION=RELEASE python genenv.py
 

CMD ["pipenv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8888"]