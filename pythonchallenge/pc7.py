# http://www.pythonchallenge.com/pc/def/oxygen.html


import urllib.request as req
import io
from PIL import Image


url = r"http://www.pythonchallenge.com/pc/def/oxygen.png"

with req.urlopen(url) as response:
    z = response.read()

img = Image.open(io.BytesIO(z))

print(img.width, " x ", img.height)

t = img.getpixel((0,0))

row = [img.getpixel((x, img.height / 2)) for x in range(img.width)]

row = row[::7]

chars = [r for r, g, b, a in row if r == g == b]

msg = "".join(map(chr, chars))

print(msg)

chars = [105, 110, 116, 101, 103, 114, 105, 116, 121]
msg2 = "".join(map(chr, chars))

print(msg2)
