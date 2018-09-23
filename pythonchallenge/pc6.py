# http://www.pythonchallenge.com/pc/def/channel.html

import urllib.request as req
import zipfile
import io

url = r"http://www.pythonchallenge.com/pc/def/channel.zip"

with req.urlopen(url) as response:
    z = response.read()

with zipfile.ZipFile(io.BytesIO(z)) as thezip:
    files = thezip.infolist()

    dict = {}
    comn = {}

    print(type(files))
    for file in files:
        key = file.filename
        val = thezip.open(file).read()
        com = thezip.getinfo(file.filename).comment.decode("utf-8")
        dict[key] = val
        comn[key] = com
        # print(key, val)

    n = 90052
    f = "{}.txt"

    comments = []

    while f.format(n) in dict:
        t = dict[f.format(n)].decode("utf-8")
        print(n, t)
        comments.append(comn[f.format(n)])
        del dict[f.format(n)]
        n = t.split(" ")[-1]

    print("".join(comments))



# 90052

