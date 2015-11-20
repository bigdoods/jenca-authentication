FROM python

ADD . /authentication
WORKDIR /authentication
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python authentication/authentication.py
