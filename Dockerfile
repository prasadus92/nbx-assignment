FROM python:3.7

COPY ./userservice /app/userservice
COPY ./config/userservice-docker.yaml /app/config/userservice.yaml
COPY ./init_db.py /app/init-db.py
COPY ./wait-for-postgres.sh /app/wait-for-postgres.sh
COPY ./run-application.sh /app/run-application.sh
COPY ./setup.py /app
RUN apt-get update && apt-get install -y postgresql-client-11
RUN ["chmod", "+x", "/app/wait-for-postgres.sh"]
RUN ["chmod", "+x", "/app/run-application.sh"]

WORKDIR /app
RUN python setup.py develop

EXPOSE 8080