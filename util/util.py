__author__ = 'quocle'

def get_last_elements(n, lines):
    if n >= len(lines):
        return lines
    return lines[-n:]

def items_in_list(items, lines):
    count = 0
    for item in items:
        for line in lines:
            if item in line:
                print item
                count = count + 1
    return count == len(items)

