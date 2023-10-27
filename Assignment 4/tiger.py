import struct

# Tiger constants
TIGER_SBOXES = [
    # S-box values would be added here
]

TIGER_INIT = (0x0123456789ABCDEF, 0xFEDCBA9876543210, 0xF096A5B4C3B2E187)

MASK64 = 0xFFFFFFFFFFFFFFFF

def xor(a, b):
    return a ^ b

def add(a, b):
    return (a + b) & MASK64

def mul8(a):
    return ((a << 8) & MASK64) | (a >> (64 - 8))

def tiger_round(a, b, c, x, mul):
    c = xor(c, x)
    a -= TIGER_SBOXES[0][c & 0xFF] ^ TIGER_SBOXES[1][(c >> 16) & 0xFF] ^ TIGER_SBOXES[2][(c >> 32) & 0xFF] ^ TIGER_SBOXES[3][(c >> 48) & 0xFF]
    b += TIGER_SBOXES[3][(c >> 8) & 0xFF] ^ TIGER_SBOXES[2][(c >> 24) & 0xFF] ^ TIGER_SBOXES[1][(c >> 40) & 0xFF] ^ TIGER_SBOXES[0][(c >> 56) & 0xFF]
    b *= mul

    return a, b, c

def tiger_compress(state, block):
    a, b, c = state
    temp = [0]*8
    for i in range(8):
        temp[i] = struct.unpack('>Q', block[i*8:(i+1)*8])[0]

    aa, bb, cc = a, b, c
    for i in range(3):
        a, b, c = tiger_round(a, b, c, temp[0], 5)
        b, c, a = tiger_round(b, c, a, temp[1], 5)
        c, a, b = tiger_round(c, a, b, temp[2], 5)
        a, b, c = tiger_round(a, b, c, temp[3], 5)
        b, c, a = tiger_round(b, c, a, temp[4], 5)
        c, a, b = tiger_round(c, a, b, temp[5], 5)
        a, b, c = tiger_round(a, b, c, temp[6], 5)
        b, c, a = tiger_round(b, c, a, temp[7], 5)

        temp = [temp[i] for i in [7,6,5,4,3,2,1,0]]

    a = xor(a, aa)
    b = add(b, bb)
    c = mul8(c, cc)

    return a, b, c

def tiger_hash(message):
    # Initial hash values
    state = TIGER_INIT

    # Padding
    length = len(message) * 8
    message += b'\x01'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += struct.pack(">Q", length)

    # Process each 64-byte block
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        state = tiger_compress(state, block)

    return ''.join(map(lambda x: format(x, '016x'), state))

if __name__ == '__main__':
    msg = input("Enter the message: ").encode('utf-8')
    print(tiger_hash(msg))
