FROM python:3.7-alpine

RUN adduser -D app
RUN pip install Flask
RUN pip install Flask-Session
RUN apk add sqlite

ADD challenge/init.sh /etc/init.sh
RUN chmod 555 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/app
ADD challenge/database.db          database.db
ADD challenge/server.py            server.py
ADD challenge/templates/index.html templates/index.html
ADD challenge/templates/login.html templates/login.html

RUN chown -R root:app /home/app
RUN chmod 440 /home/app/database.db
RUN chmod 550 /home/app/templates
RUN chmod 440 /home/app/templates/index.html
RUN chmod 440 /home/app/templates/login.html
RUN chmod 550 /home/app/server.py

USER app
