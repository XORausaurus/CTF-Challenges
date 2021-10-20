FROM python:3.7-alpine

RUN apk --no-cache add socat gcc musl-dev gmp-dev
RUN pip install pycryptodome

ADD challenge/server.py server.py
ADD challenge/flag.py flag.py

CMD socat TCP-L:9999,fork,reuseaddr EXEC:"python server.py"
