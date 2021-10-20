# zer0pts CTF 2021 · Challenge: Subleq64


## Files

* `challenge/`
    * `hsq.cpp` (Higher Subleq compiler from [[1]]: C-like lang → Subleq bytecode)
    * `mkflag.py` (flag decryptor and encryptor)
    * `subleq64.hsq` (challenge itself)
    * `bin/runsq64` (simple Subleq64 emulator)


## Building

Compile the compiler:

```
subleq64$ cd challenge/
subleq64/challenge$ make hsq
g++     hsq.cpp   -o hsq
```

Compile the challenge:

```
subleq64/challenge$ ./hsq -q subleq64.hsq -o | bin/postprocess-sq >../rawdistfiles/subleq64.sq
```


## Testing

Run `./challenge/bin/runsq64 ./rawdistfiles/subleq64.sq`. It should start printing the flag:

```
subleq64$ ./challenge/bin/runsq64 ./rawdistfiles/subleq64.sq
zer0pts{O
```

---

Checklist:

* confirm that the output of `mkflag.py encrypt slow` matches the output of `mkflag.py encrypt fast`
* confirm that the output of `mkflag.py decrypt slow` matches the output of `mkflag.py decrypt fast`
* confirm that `flag_ciphertext` in `mkflag.py` matches the output of `mkflag.py encrypt fast`
* confirm that `flag_plaintext` in `mkflag.py` matches the output of `mkflag.py decrypt fast`
* confirm that `m`, `a`, `c` and `seed` in `subleq64.hsq` and `mkflag.py` match each other
* confirm that `flag` in `subleq64.hsq` matches `flag_ciphertext` in `mkflag.py`
* confirm that the algo in `subleq64.hsq` is equivalent to `mkflag.py decrypt slow`
* confirm that `flag` in `task.yml` matches `flag_plaintext` in `mkflag.py`

---

`rawdistfiles/subleq64.sq` should contain only one line, no double spaces, no leading or trailing spaces:

```
subleq64$ python3
[...]
>>> with open('rawdistfiles/subleq64.sq') as f: data = f.read()
... 
>>> from collections import Counter
>>> Counter(data)
Counter({' ': 6178, '6': 4686, '1': 4235, '7': 2732, '4': 2099, '8': 1772, '0': 1607, '3': 1579, '5': 1470, '2': 1424, '9': 1377, '-': 8, '\n': 1})
>>> data.endswith('\n')
True
>>> '  ' in data
False
>>> data.startswith(' ')
False
>>> data.endswith(' \n')
False
```


## Links

1. http://mazonka.com/subleq/hsq.cpp
2. https://esolangs.org/wiki/Subleq
3. https://esolangs.org/wiki/Higher_Subleq

[1]: http://mazonka.com/subleq/hsq.cpp
