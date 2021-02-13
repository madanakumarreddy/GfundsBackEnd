FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /cod
WORKDIR /cod
ADD requirements.txt /cod/
RUN pip install -r requirements.txt
ADD . /cod/

