# Project Euler problem 2

(a, b) = (1, 2)

s = 0
while a < 4e6:
    #print(a, b)
    if a % 2 == 0:
        s += a
    (a, b) = (b, a+b)

print(s)