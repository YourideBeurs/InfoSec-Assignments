import sys
import struct

def feistel_function(data: int, key: bytes) -> int:
    return int.from_bytes(key, byteorder='little')

def feistel_cipher(key: bytes, data: bytes, mode: str) -> bytes:
    if len(data) % 8 != 0:
        raise ValueError("Data length must be a multiple of 8 bytes")

    output = bytearray()

    # Process each 8-byte block
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        LH, RH = struct.unpack('<II', block)

        # Number of rounds is the length of the key divided by 4
        for j in range(0, len(key), 4):
            LH, RH = RH, LH ^ feistel_function(RH, key[j:j+4])

        output.extend(struct.pack('<II', LH, RH))

    return output

def main():
    content = sys.stdin.buffer.read()
    mode_data, key, data = [part for part in content.split(b'\xFF',2) if part]
    mode = 'e' if mode_data == b'e' else 'd'
    result = feistel_cipher(key, data, mode)
    sys.stdout.buffer.write(result)

if __name__ == "__main__":
    main()