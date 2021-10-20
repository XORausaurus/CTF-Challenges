FROM ubuntu:18.04

RUN apt update && apt install -y build-essential g++ libgmp-dev libssl-dev python3 python3-dev python3-pip
RUN pip3 install pycryptodome ptrlib

ADD findkey.cpp findkey.cpp
RUN g++ findkey.cpp -o findkey -lcrypto
ADD solve.py solve.py

CMD python3 solve.py
