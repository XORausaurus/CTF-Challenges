    1  2021-09-24 18:35:08 ls -la
    2  2021-09-24 18:35:11 touch password
    3  2021-09-24 18:35:20 python3 passwordgen.py 16 > password
    4  2021-09-24 18:35:42 zip --password $(cat password) data.zip flag.txt
    5  2021-09-24 18:35:46 cat password
    6  2021-09-24 18:35:57 srm -vz password
    7  2021-09-24 18:36:06 srm -vz flag.txt