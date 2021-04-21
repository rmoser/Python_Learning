# http://www.pythonchallenge.com/pc/return/good.html

import urllib
import urllib.request as req
import io
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt


url = r"http://www.pythonchallenge.com/pc/return/good.jpg"

password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
opener.open(url)
urllib.request.install_opener(opener)

with req.urlopen(url) as response:
    z = response.read()

img = Image.open(io.BytesIO(z))

print(img.width, " x ", img.height)

t = img.getpixel((0,0))

print(img.width)
print(img.height)

zeros = []

p = img.getpixel((639,420))
print(p)

for y in range(10, img.height - 30):
    for x in range(10, img.width - 30):
        (r, g, b) = img.getpixel((x, y))
        if (r < 20 and g < 20 and b < 20):
            zeros.append((x,y))

print(zeros)
print(zip(zeros))

data = np.array(zeros)

plt.scatter(*zip(*data), s=1)
plt.gca().invert_yaxis()
plt.show()

# pixels = [zeros.append(x,y) if img.getpixel((x, y)) for x in range(img.width) for y in range(img.height)]

# print(pixels)

# chars = [r for r, g, b, a in row if r == g == b]

# msg = "".join(map(chr, chars))s

# print(msg)

# chars = [105, 110, 116, 101, 103, 114, 105, 116, 121]
# msg2 = "".join(map(chr, chars))

# print(msg2)
