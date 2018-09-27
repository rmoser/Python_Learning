import math

'''
    polysum(n, s)

    Purpose: For a regular polygon with n sides, each of length s,
        returns the Area of the polygon, plus the square of the Perimeter
        Result is rounded to 4 decimal places

    Arguments:
        n: number of sides for the polygon
        s: length of each side of the polygon

'''
def polysum(n, s):
    # Catch invalid inputs
    # Non-numbers are invalid
    if not isinstance(n, (int, float)) or not isinstance(s, (int, float)):
        return 0

    # Negative numbers are invalid, and zero sides would cause a divide by zero error
    if n <= 0 or s <= 0:
        return 0

    # Calculate Area of a polygon with n sides, each of length s
    area = 0.25 * n * s ** 2 / math.tan(math.pi / n)

    # Calculate Perimeter of a polygon with n sides, each of length s
    perimeter = n * s

    # Return Area + square of Perimeter, because that's what the teacher requested it should do
    # Rounded to 4 significant digits
    return round(area + perimeter ** 2, 4)

