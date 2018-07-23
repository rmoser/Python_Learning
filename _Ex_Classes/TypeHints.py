# No variable type hints:
def minus(x, y):
    return x - y

# Variable type hints:
def plus(x: int, y: int) -> int:
    return x + y

print(plus(1,2))
print(minus(1,2))

# Note highlights for incorrect argument type:
print(plus("A", "B"))

try:
    print(minus("A", "B"))
except:
    pass

# Note highlights for incorrect argument type:
print(plus(1.2, 2.4))
print(minus(1.2, 2.4))

s = plus(1.2, 2.4)
print(s)

print(format(s, '.1f'))



