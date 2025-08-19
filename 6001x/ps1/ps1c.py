def get_ordered_string(s):
    result = ''
    pstart = 0
    pend = 1
    end = len(s)
    for i in range(1, end):
        if s[i] >= s[i-1] or i == end:
            pend = i+1
            r = s[pstart:pend]
        else:
            r = s[pstart:pend]
            pstart = i
            pend = i+1

        if len(r) > len(result):
            result = r

        print(i, pstart, pend, s[pstart:pend], r, result, len(r), len(result))
    return result

print(get_ordered_string('abcammvcba'))
print(get_ordered_string('ycuspehyyexibwddddh'))

