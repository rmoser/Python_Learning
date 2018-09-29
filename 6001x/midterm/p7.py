# 6.00.1x midterm p7

def general_poly(L):
    """ L, a list of numbers (n0, n1, n2, ... nk)
    Returns a function, which when applied to a value x, returns the value
    n0 * x^k + n1 * x^(k-1) + ... nk * x^0 """

    # Use list comprehension
    # Iterate on L in reverse so the '0' item in the list is the coefficient for the 0-power term
    # Return lambda function
    return lambda x: sum(num * x ** idx for idx, num in enumerate(L[::-1]))


a = general_poly([1,2,3,4])
print(a(10))
print(a(0))
print(a(1))
