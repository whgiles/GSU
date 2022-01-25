FROM postgres:13.2

ENV POSTGRES_PASSWORD=wsb
ENV POSTGRES_USER=wsb
ENV POSTGRES_DB=wsb

COPY wsb.sql /docker-entrypoint-initdb.d/
EXPOSE 5432