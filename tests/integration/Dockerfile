FROM python:3-alpine
RUN mkdir /test
WORKDIR /test
ADD requirements.txt /test/
RUN pip install -r requirements.txt
ADD . /test/
