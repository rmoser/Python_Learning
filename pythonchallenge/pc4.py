# http://www.pythonchallenge.com/pc/def/linkedlist.php

import urllib.request as req

url = r"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={}"

n = 12345

for i in range(1, 400):
    u = url.format(n)
    print(i, u)

    with req.urlopen(u) as response:
        html = response.read().decode("utf-8")
        n = html.split(" ")[-1]



