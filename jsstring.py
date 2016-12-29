from sys import argv

fin = open(argv[1], "rb")
data = fin.read()
fin.close()

s = ""

for x in range(0, len(data), 2):
    t = hex(data[x] + 256 * data[x + 1])[2:]
    while len(t) < 4:
        t = '0' + t
    s += r"\u" + t

print('"{}"'.format(s))
