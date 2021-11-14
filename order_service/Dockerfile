ARG SERVICE_NAME

FROM python:3.11.0a1-alpine3.14

RUN pip install prometheus_client==0.12.0
RUN pip install flask==2.0.2
RUN pip install redis==3.5.3
RUN pip install requests==2.26.0

COPY . .

ENV SERVICE_NAME=order_service

RUN mkdir -p /app

ENV FLASK_ENV development
ENV FLASK_APP /app/${SERVICE_NAME}/${SERVICE_NAME}.py
ENV PYTHONPATH /app

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
