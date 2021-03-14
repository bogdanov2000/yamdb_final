FROM python:3.8.5
WORKDIR /code
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir
COPY . .
ENTRYPOINT [ "/code/entrypoint.sh" ]
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

