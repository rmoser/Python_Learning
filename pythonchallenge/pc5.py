# http://www.pythonchallenge.com/pc/def/peak.html

import pickle
import urllib.request as req

url = r"http://www.pythonchallenge.com/pc/def/peak.html"
pic = r"http://www.pythonchallenge.com/pc/def/peakhell.jpg"
ban = r"http://www.pythonchallenge.com/pc/def/banner.p"

with req.urlopen(ban) as response:
    pickled = response.read()

print(pickled)

data = pickle.loads(pickled)

for line in data:
    print("".join([k*v for k, v in line]))






