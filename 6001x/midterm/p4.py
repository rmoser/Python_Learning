# 6.00.1x midterm p4

def dotProduct(listA, listB):
    '''
    listA: a list of numbers
    listB: a list of numbers of the same length as listA
    '''

    # zip will intertwine the two lists, so the resulting iterable object looks something like:
    # ( (listA[0], listB[0]), (listA[1], listB[1]), ... , (listA[N], listB[N]) )
    return sum(a * b for a, b in zip(listA, listB))

a = [1, 2, 3]
b = [4, 5, 6]

print(dotProduct(a, b))


c = [-1, 0, 1]
d = [4, 5, 6]

print(dotProduct(c, d))
