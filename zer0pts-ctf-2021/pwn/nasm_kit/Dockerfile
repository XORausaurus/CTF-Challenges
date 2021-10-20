FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install xinetd
RUN apt-get -y install python3 nasm
RUN groupadd -r pwn && useradd -r -g pwn pwn

ADD challenge/pwn.xinetd /etc/xinetd.d/pwn
ADD challenge/init.sh    /etc/init.sh
ADD challenge/redir.sh   /home/pwn/redir.sh
ADD distfiles/bin/libunicorn.so.1 /usr/lib/libunicorn.so.1
RUN chmod 550 /home/pwn/redir.sh
RUN chmod 500 /etc/init.sh
RUN chmod 755 /usr/lib/libunicorn.so.1
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
ADD challenge/flag.txt     flag.txt
ADD distfiles/bin/x64-emulator x64-emulator
ADD distfiles/bin/server.py    server.py
RUN chmod 440 flag.txt
RUN chmod 550 x64-emulator
RUN chmod 550 server.py
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt

RUN chown -R root:pwn /home/pwn

RUN service xinetd restart
