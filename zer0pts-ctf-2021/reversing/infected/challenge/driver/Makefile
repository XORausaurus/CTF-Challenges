CFLAGS=-Wall -O0

backdoor: main.c
	gcc $(CFLAGS) main.c `pkg-config fuse --cflags --libs` -o backdoor

clean:
	rm *.o
