FROM python:3.8.5

RUN mkdir /home/reservproject

COPY ./requirements.pip /home/reservproject

WORKDIR /home/reservproject
EXPOSE 8000
RUN pip install -r requirements.pip