FROM ubuntu:trusty

ADD . /authentication
WORKDIR /authentication

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python authentication/authentication.py
