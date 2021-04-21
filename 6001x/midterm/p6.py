# 6.00.1x p6

def flatten(aList):
    '''
    aList: a list
    Returns a copy of aList, which is a flattened version of aList
    '''

    result = []  # Empty list

    # Iterate on items in aList
    for x in aList:
        # For any list item, recurse flatten(x), and use + operator to append the resulting list
        #   which will have only one level
        if isinstance(x, list):
            result += flatten(x)

        # For anything other than a list, append it to result
        else:
            result.append(x)
    return result

