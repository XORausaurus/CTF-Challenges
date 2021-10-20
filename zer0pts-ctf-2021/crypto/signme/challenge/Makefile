all: main.o signme.o
	gcc main.o signme.o -o chall -lgmp -static

main.o: main.c signme.h
	gcc -c main.c -o main.o

signme.o: signme.c signme.h
	gcc -c signme.c -o signme.o
