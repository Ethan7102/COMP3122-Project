ARG SERVICE_NAME

FROM python:3

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV SERVICE_NAME=menu_service

RUN mkdir -p /app

ENV FLASK_ENV development
ENV FLASK_APP /app/${SERVICE_NAME}/${SERVICE_NAME}.py
ENV PYTHONPATH /app

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]