from sys import argv

data_base = -1
data_written = b""

def set_data_base(x):
    global data_base
    data_base = x
    return "/* data_base set to 0x{:x} */".format(x)

def writes(s):
    if data_base < 0:
        raise Exception("data_base not initialized")
    global data_written
    prev_len = len(data_written)
    data_written += s.encode("utf-8") + b"\x00"
    return hex(data_base + prev_len)

def bruteforce_syscall():
    tpl = """
        memset(ENCDEC_SCRATCH + 0x1000,0,0x10);
        memset(ENCDEC_SCRATCH + 0x800,0,0x30);
        store(ENCDEC_SCRATCH + 0x1000, ENCDEC_SCRATCH);
        store(ENCDEC_SCRATCH + 0x1000, ENCDEC_SCRATCH + 0x4);
        store(0x10, ENCDEC_SCRATCH + 0x8);
        store(ENCDEC_SCRATCH + 0x800, ENCDEC_SCRATCH + 0xC);
        store(0, ENCDEC_SCRATCH + 0x10); // was: store(0x100, ENCDEC_SCRATCH + 0x10);
        store(ENCDEC_SCRATCH + 0x820,ENCDEC_SCRATCH + 0x14);
        set_syscall({syscall});
        syscall(ENCDEC_SCRATCH, 0x10000, 0xA);
        store(RET, OUTPUT + 16 * {idx});
        store({syscall}, OUTPUT + 4 + 16 * {idx});
        memcpy(OUTPUT + 8 + 16 * {idx}, ENCDEC_SCRATCH + 0x1000, 0x8);
    """
    res = ""
    start = 0x2c0 - 0x20  # 0x30 * 3
    for idx in range(0x50):
        syscall = start + idx
        res += tpl.format(syscall=syscall, idx=idx)
    return res

def bruteforce_kx():
    tpl = """
        memset(ENCDEC_SCRATCH + 0x4000,0,0x100);
        memset(ENCDEC_SCRATCH + 0x800,0,0x30);
        store(ENCDEC_SCRATCH + 0x4000, ENCDEC_SCRATCH);
        store(ENCDEC_SCRATCH + 0x4000, ENCDEC_SCRATCH+0x4);
        store(0x20,ENCDEC_SCRATCH+0x8);
        loadret(MEMBLOCK_BASE);
        addret(0x1FF68);
        storeret(ENCDEC_SCRATCH+0xC);
        store(0x4E0,ENCDEC_SCRATCH+0x10);
        store(0,ENCDEC_SCRATCH+0x14);
        svc({syscall}, ENCDEC_SCRATCH, 0x3f, 0);
    """
    res = ""
    start = 0x2c0
    for idx in range(0x50):
        syscall = start + idx
        res += tpl.format(syscall=syscall)
    return res

class Eval:

    def __getitem__(self, key):
        try:
            return eval(key)
        except:
            print("Evaluating {} failed".format(key))
            raise

def write_bin(data, addr):
    split = [data[i:i+4] for i in range(0, len(data), 4)]
    output = ""
    for idx, chunk in enumerate(split):
        output += "store({}, {});".format(int.from_bytes(chunk, byteorder="little"), addr + 4 * idx)
    return output

fin = open(argv[1], "r")
data = fin.read()
fin.close()

data = data % Eval()
data = data.replace("$writedata$", write_bin(data_written, data_base))
data = data.replace("$nopsled$", "store(0, 0x89000000);" * 30)

fout = open(argv[2], "w")
fout.write(data)
fout.close()
