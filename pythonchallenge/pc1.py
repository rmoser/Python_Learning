# http://www.pythonchallenge.com/pc/def/map.html



s = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."

dict = {}

stin = ""
for c in range(97, 123):
    stin += chr(c)

stout = stin[2:]+stin[0:2]

print(stin)
print(stout)

trantab = str.maketrans(stin, stout)

print(s.translate(trantab))

print("map".translate(trantab))



