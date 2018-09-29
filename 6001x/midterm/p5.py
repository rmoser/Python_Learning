# 6.00.1x midterm p5

def dict_invert(d):
    '''
    d: dict
    Returns an inverted dictionary according to the instructions above
    '''
    result = {}  # Empty dict

    # Loop on key, value pairs
    # Sort the keys first, so we don't have to sort them when inserting into lists as values in the inverted dict
    for key in sorted(d):  # Iterating on a dict defaults to the keys, so d.keys() is redundant
        # Store the value for key, since we use it more than once
        value = d[key]

        # If this is the first instance of value, create a list to store all keys that point to it in the input dict d
        if value not in result:
            # Inverting key, value
            result[value] = [key]

        # If value exists as a key, then append to the list
        # Since the keys were already sorted, append will correctly add new keys at the end of the list
        else:
            result[value].append(key)

    return result


print(dict_invert({1:10, 2:20, 3:30}))
print(dict_invert({1:10, 2:20, 3:30, 4:30}))
print(dict_invert({4:True, 2:True, 0:True}))

print(dict_invert({6:10, 2:20, 3:10, 9:30, 8:10, 99:30}))
