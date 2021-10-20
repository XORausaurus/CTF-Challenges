all:
	gcc -Wl,-z,lazy,-z,relro main.c -o chall -fstack-protector-all -no-pie
	mv chall ../distfiles
	cp main.c ../distfiles
