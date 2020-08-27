FROM python:3.6.10-alpine3.11
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY . /usr/src/app/
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "webhook.py" ]

EXPOSE 5000
