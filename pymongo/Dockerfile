FROM python:3.8

RUN pip install pymongo rich

COPY app/. /app

ENTRYPOINT [ "tail", "-F", "/doesnt-matter" ]