

STR_DATA = b'\x01\x01\xa6\x0c\x9c\xaa\xe8\x11\xe7\x11\xab\x12\x18\x17\xa3\x15\xb8\x15\x9f\x16\x0e\xb4\x00\x00\x00\x00\x00\x00'

ba = bytearray(STR_DATA)
res = [0] * 14
j = 0
for i in range(0, 28, 2):
    res[j] = int(ba[i]) + ( int(ba[i+1]) << 8 )
    print(res[j])
    j += 1


