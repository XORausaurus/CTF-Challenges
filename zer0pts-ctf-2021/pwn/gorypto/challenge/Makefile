all:
	go build -a -ldflags='-s -w -extldflags "-static"' main.go
	upx -9 main
	cp main.go ../distfiles/main.go
	mv main ../distfiles/chall
