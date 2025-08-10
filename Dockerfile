FROM python:3.13.6-alpine3.21 AS prod

WORKDIR /app

COPY requirements.txt .

RUN apk update \
    & apk upgrade \
    & apk add cloud-init \
    & apk add --no-cache build-base dbus-dev glib-dev

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "dev"]