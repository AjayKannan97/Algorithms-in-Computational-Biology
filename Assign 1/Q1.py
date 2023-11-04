import sys

def getZarr(string, z):
    n = len(string)
    l, r, k = 0, 0, 0
    for i in range(1, n):
        if i > r:
            l, r = i, i
            while r < n and string[r - l] == string[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z

def search(text, pattern):
    string = pattern + "$" + text # Create concatenated string "P$T"
    #print(len(string))
    l = len(string)
    z = [0] * l
    z = getZarr(string, z)
    length = max(z)
    k = []
    for i in range(l):
        if z[i] == length: # if Z[i] (matched region) is equal to pattern
            k.append(i - length - 1)
    return k



            
for arg in range(1,16):
    a = str(sys.argv[arg])
    print(a)
    file1 = open('samples/sample_'+a, 'r')
    Lines = file1.readlines()
    d = []
    for line in Lines:
        line = line.replace(" ", "")
        #print(len(line))
        d.append(line)

    text = d[0]
    pattern = d[1]
    lines = search(text, pattern)
    print(lines)
    with open('output/sol_'+a, 'w') as f:
        for l in lines:
            f.write(str(l)+'\n')