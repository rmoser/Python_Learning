# http://www.pythonchallenge.com/pc/def/integrity.html



import urllib.request as req
import bz2
import re

url = r"http://www.pythonchallenge.com/pc/def/integrity.html"
portal = r"http://www.pythonchallenge.com/pc/return/good.html"

pattu = r"un: (.*)"
pattp = r"pw: (.*)"

with req.urlopen(url) as response:
    z = str(response.read().decode("utf-8"))

    print(z)

    un = re.findall(pattu, z)[0][1:-1].encode("utf-8")
    pw = re.findall(pattp, z)[0][1:-1].encode("utf-8")

print("un: ", un)
print("pw: ", pw)


# How to do this conversion in Python???
username = bz2.decompress(b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084')
password = bz2.decompress(b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08')

print("USER: ", username)
print("PASS: ", password)
