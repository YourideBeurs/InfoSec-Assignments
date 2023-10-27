import struct
import sys

from sboxes import t1, t2, t3, t4

TIGER_SBOXES = [t1, t2, t3, t4]

TIGER_INIT = (0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187)

MASK64 = 0xFFFFFFFFFFFFFFFF

def moduloMask(data):
    return (data % 2^64) & MASK64

def key_schedule(w):
    w[0] -= moduloMask(w[7] ^ 0xA5A5A5A5A5A5A5A5)
    w[1] ^= moduloMask(w[0])
    w[2] += moduloMask(w[1])
    w[3] -= moduloMask(w[2] ^ ((~w[1]) << 19))
    w[4] ^= moduloMask(w[3])
    w[5] += moduloMask(w[4])
    w[6] -= moduloMask(w[5] ^ ((~w[4]) >> 23))
    w[7] ^= moduloMask(w[6])
    w[0] += moduloMask(w[7])
    w[1] -= moduloMask(w[0] ^ ((~w[7]) << 19))
    w[2] ^= moduloMask(w[1])
    w[3] += moduloMask(w[2])
    w[4] -= moduloMask(w[3] ^ ((~w[2]) >> 23))
    w[5] ^= moduloMask(w[4])
    w[6] += moduloMask(w[5])
    w[7] -= moduloMask(w[6] ^ 0x0123456789ABCDEF)

def xor(a, b):
    return a ^ b

def add(a, b):
    return ((a + b) % 2^64) & MASK64

def mul8(a):
    return (((a << 8) % 2^64) & MASK64) | (a >> (64 - 8))

def tiger_round(a, b, c, x, mul):
    c = xor(c, x)
    a = ((a - TIGER_SBOXES[0][c & 0xFF] ^ TIGER_SBOXES[1][(c >> 16) & 0xFF] ^ TIGER_SBOXES[2][(c >> 32) & 0xFF] ^ TIGER_SBOXES[3][(c >> 48) & 0xFF]) % 2^64) & MASK64
    b = ((b + TIGER_SBOXES[3][(c >> 8) & 0xFF] ^ TIGER_SBOXES[2][(c >> 24) & 0xFF] ^ TIGER_SBOXES[1][(c >> 40) & 0xFF] ^ TIGER_SBOXES[0][(c >> 56) & 0xFF] ) % 2^64) & MASK64
    b = ((b * mul) % 2^64) & MASK64

    return a, b, c

def tiger_compress_2_0(state, block):
    a, b, c = state
    temp = [0]*8
    for i in range(8):
        temp[i] = struct.unpack('<Q', block[i*8:(i+1)*8])[0]
    
    aa, bb, cc = a, b, c
    tiger_round(a, b, c, block[0], 5)
    tiger_round(b, c, a, block[1], 5)
    tiger_round(c, a, b, block[2], 5)
    tiger_round(a, b, c, block[3], 5)
    tiger_round(b, c, a, block[4], 5)
    tiger_round(c, a, b, block[5], 5)
    tiger_round(a, b, c, block[6], 5)
    tiger_round(b, c, a, block[7], 5)
    key_schedule(block)
    tiger_round(c, a, b, block[0], 7)
    tiger_round(a, b, c, block[1], 7)
    tiger_round(b, c, a, block[2], 7)
    tiger_round(c, a, b, block[3], 7)
    tiger_round(a, b, c, block[4], 7)
    tiger_round(b, c, a, block[5], 7)
    tiger_round(c, a, b, block[6], 7)
    tiger_round(a, b, c, block[7], 7)
    key_schedule(block)
    tiger_round(b, c, a, block[0], 9)
    tiger_round(c, a, b, block[1], 9)
    tiger_round(a, b, c, block[2], 9)
    tiger_round(b, c, a, block[3], 9)
    tiger_round(c, a, b, block[4], 9)
    tiger_round(a, b, c, block[5], 9)
    tiger_round(b, c, a, block[6], 9)
    tiger_round(c, a, b, block[7], 9)

    a = moduloMask(a ^ aa)
    b = moduloMask(b - bb)
    c = moduloMask(c + cc)
    # a = xor(a, aa)
    # b = add(b, bb)
    # c = ((c + cc) % 2^64) & MASK64

    return a, b, c

def tiger_compress(state, block):
    a, b, c = state
    temp = [0]*8
    for i in range(8):
        temp[i] = struct.unpack('<Q', block[i*8:(i+1)*8])[0]

    aa, bb, cc = a, b, c
    getal = [5, 7, 9]
    for i in range(3):
        a, b, c = tiger_round(a, b, c, temp[0], getal[i])
        b, c, a = tiger_round(b, c, a, temp[1], getal[i])
        c, a, b = tiger_round(c, a, b, temp[2], getal[i])
        a, b, c = tiger_round(a, b, c, temp[3], getal[i])
        b, c, a = tiger_round(b, c, a, temp[4], getal[i])
        c, a, b = tiger_round(c, a, b, temp[5], getal[i])
        a, b, c = tiger_round(a, b, c, temp[6], getal[i])
        b, c, a = tiger_round(b, c, a, temp[7], getal[i])
        a, b, c = b, c, a

        temp = [temp[i] for i in [7,6,5,4,3,2,1,0]]

    a = xor(a, aa)
    b = add(b, bb)
    c = ((c + cc) % 2^64) & MASK64

    return a, b, c

def tiger_hash(message):
    # Initial hash values
    state = TIGER_INIT

    # Padding
    length = len(message) * 8
    message += b'\x01'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += struct.pack("<Q", length)

    # Process each 64-bit block
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        state = tiger_compress_2_0(state, block)

    byte_string = b''.join(struct.pack('Q', num) for num in state)
    # print(byte_string)
    # print(byte_string.decode('utf-8'))
    sys.stdout.buffer.write(byte_string)

    # return ''.join(map(lambda x: format(x, '016x'), state))
    # result =  b''.join(map(lambda x: x.to_bytes(8, 'little'), state))
    # print(type(result))
    # print()
    # print(result)

def main():
    msg = input().encode('utf-8')
    print(tiger_hash(msg))

if __name__ == '__main__':
    main()