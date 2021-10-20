chall:
	gcc main.c -o ../distfiles/chall -O3 -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast

run:
	echo '${SECRET}'
	echo '${SECRET}' | ../distfiles/chall > ../distfiles/output.txt
