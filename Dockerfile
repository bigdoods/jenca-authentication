# Start from the Python image so that we have Python tools like `pip` available.
FROM python

ADD . /authentication
WORKDIR /authentication

# Installing the requirements like this is convenient for now, but means that
# requirements are not cached and so have to be downloaded each time.
RUN pip install -r requirements.txt

# 5000 is the default port which Flask runs on, but this might not be suitable
# in production.
EXPOSE 5000

CMD python authentication/authentication.py
