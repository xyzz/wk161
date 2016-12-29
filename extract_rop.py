from sys import argv, exit

fin = open(argv[1], "rb")
data = fin.read()
fin.close()

dsize = int.from_bytes(data[0x10:0x18], byteorder="little")
if dsize != 0:
    print("Data section has to be empty")
    exit(1)
csize = int.from_bytes(data[0x20:0x28], byteorder="little")
rop = data[0x30:0x30+csize]

fout = open(argv[2], "wb")
fout.write(rop)
fout.close()
