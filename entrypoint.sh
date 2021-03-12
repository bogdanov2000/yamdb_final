#!/bin/sh
apk update && apk add postgresql-dev gcc python3-dev musl-dev
python -m pip install --upgrade pip && pip install -r requirements.txt
sleep 20
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata fixtures.json
exec "$@"