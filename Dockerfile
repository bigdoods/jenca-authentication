# Start from the Python image so that we have Python tools like `pip` available.
FROM python

WORKDIR /authentication

# Add requirements file first so that requirements are only re-installed if the
# requirements file changes, instead of if anything in the project changes.
ADD ./requirements.txt /authentication/requirements.txt
RUN pip install -r requirements.txt

ADD . /authentication

# 5000 is the default port which Flask runs on, but this might not be suitable
# in production.
EXPOSE 5000

CMD python authentication/authentication.py
