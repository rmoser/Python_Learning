# Library funcs for 6.00.1 Final Exam

def add_func(x, y):
    return x + y

# Problem 3
def sum_digits(s):
    digits = [int(c) for c in s if c in "0123456789"]

    if len(digits) == 0:
        raise ValueError

    return sum(digits)


# Problem 4
def primes_list(N):
    '''
    N: an integer
    '''

    result = []

    for n in range(2, N+1):
        if not any(n % d == 0 for d in result):
            result.append(n)

    return result

# Problem 5
def uniqueValues2(aDict):
    '''
    aDict: a dictionary
    returns: a sorted list of keys that map to unique aDict values, empty list if none
    '''


    workDict = dict()
    for k in aDict:
        v = aDict[k]
        if v not in workDict:
            workDict[v] = [k]
        else:
            workDict[v].append(k)

    return sorted([v[0] for k, v in workDict.items() if len(v) == 1])


def uniqueValues(aDict):
    '''
    aDict: a dictionary
    returns: a sorted list of keys that map to unique aDict values, empty list if none
    '''
    return sorted([k for k, v in aDict.items() if list(aDict.values()).count(v) == 1])


# Problem 6
class Person(object):
    def __init__(self, name):
        self.name = name

    def say(self, stuff):
        return self.name + ' says: ' + stuff

    def __str__(self):
        return self.name


class Lecturer(Person):
    def lecture(self, stuff):
        return 'I believe that ' + Person.say(self, stuff)


class Professor(Lecturer):
    def say(self, stuff):
        return self.name + ' says: ' + self.lecture(stuff)


class ArrogantProfessor(Professor):
    def say(self, stuff):
        return Person.say(self, self.lecture(stuff))

    def lecture(self, stuff):
        return 'It is obvious that ' + Person.say(self, stuff)

# Problem 7
class myDict(object):
    """ Implements a dictionary without using a dictionary """

    def __init__(self):
        """ initialization of your representation """
        self._keys = []
        self._values = []

    def assign(self, k, v):
        """ k (the key) and v (the value), immutable objects  """
        if k not in self._keys:
            self._keys.append(k)
            self._values.append(v)
        else:
            i = self._keys.index(k)
            self._values[i] = v

    def getval(self, k):
        """ k, immutable object  """
        if k not in self._keys:
            raise KeyError
        i = self._keys.index(k)
        return self._values[i]

    def delete(self, k):
        """ k, immutable object """
        if k not in self._keys:
            raise KeyError
        i = self._keys.index(k)
        del self._keys[i]
        del self._values[i]
