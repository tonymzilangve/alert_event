FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /consumer
WORKDIR /consumer

RUN apk --update add gcc libc-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7000

CMD python -m nats_mq.consumer.consumer 0.0.0.0:7000
