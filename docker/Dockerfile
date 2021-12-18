FROM python:3.8-alpine

RUN apk update && apk add curl 

WORKDIR /app

RUN curl https://bootstrap.pypa.io/get-pip.py | python && \
    pip install --upgrade setuptools

COPY ./requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt

COPY . /app

EXPOSE 8000

CMD python main.py
