from __future__ import with_statement

s = 'failure message="Error"'                    # String to find
fname = 'output.xml'                             # File to check

def get_n_last_lines( fname, n):

    with open(fname, "r") as f:
        f.seek (0, 2)           # Seek @ EOF
        fsize = f.tell()        # Get Size
        f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
        lines = f.readlines()       # Read to end

    lines = lines[-n:]    # Get last n lines
    return lines

def find_str(find_str, lines):
    # Searching for a substring
    for line in lines:
        if find_str in line:
            print line
            return True
    return False

for line in get_n_last_lines(fname, 5):
    print line

print find_str(s, get_n_last_lines(fname, 5))