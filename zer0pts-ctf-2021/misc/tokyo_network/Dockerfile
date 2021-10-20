FROM python:3.7-alpine

RUN apk --no-cache add socat
RUN apk --no-cache add make cmake g++ git
RUN adduser -D ctf

RUN pip install qulacs
RUN pip install pycryptodome
RUN pip install numpy

ADD challenge/server.py /home/ctf/server.py
ADD challenge/secret.py  /home/ctf/secret.py
RUN chmod 500 /home/ctf/server.py
RUN chmod 400 /home/ctf/secret.py
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf
CMD socat TCP-L:11099,fork,reuseaddr EXEC:"python3 ./server.py",stderr
