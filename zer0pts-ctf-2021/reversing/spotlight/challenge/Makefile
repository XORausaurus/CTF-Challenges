CC=gcc
CFLAGS=-masm=intel -mgeneral-regs-only -mno-red-zone -O2

all: chall

chall: main.c veil.py
	$(CC) main.c -o chall $(CFLAGS)
	strip --strip-all chall
	python veil.py chall
	chmod +x obfuscated
