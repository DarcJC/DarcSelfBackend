FROM python:3.9-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.cloud.tencent.com/g' /etc/apk/repositories && \
    sed -i 's/https/http/' /etc/apk/repositories && \
    apk add --no-cache curl git && \
    pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc g++ musl-dev libc-dev postgresql-dev libffi-dev make && \
    pip install --no-cache-dir "uvicorn[standard]" && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps

COPY . .

ENTRYPOINT [ "python", "main.py", "dev" ]
