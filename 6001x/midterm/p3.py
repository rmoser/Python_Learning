# 6.00.1x midterm p3

import math

def closest_power(base, num):
    # base ** power == num
    # find the integer value where base ** value is closest to num

    # This could be done with a loop, but that seems too inefficient.
    # Also, the specification does not prescribe a loop

    # Use logarithm to calculate the exact float value
    float_ans = math.log(num)/math.log(base)

    # Test the integer values above and below the exact float value to see which is closest on the linear scale
    lo = int(float_ans)  # integer value below float_ans
    hi = lo + 1  # integer value above float_ans

    if base ** hi - num < num - base ** lo:
        # Linear delta is less for hi vs. lo
        return hi
    else:
        # Linear delta is less or equal for lo vs. hi
        return lo

print(closest_power(3, 12))
print(closest_power(4, 12))
print(closest_power(4, 1))
print(closest_power(10, 1000))
print(closest_power(9, 1000))
print(closest_power(11, 1000))
print(closest_power(100, 1000))

