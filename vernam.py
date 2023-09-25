import sys

def vernam_cipher(key: bytes, data: bytes) -> bytes:
    return bytes([k ^ d for k, d in zip(key, data)])

def main():
    content = sys.stdin.buffer.read()
    key, _, data = content.partition(b'\xFF')
    
    if len(key) != len(data):
        sys.stderr.write("Key and data lengths do not match\n")
        sys.exit(1)
        
    ciphered_data = vernam_cipher(key, data)
    sys.stdout.buffer.write(ciphered_data)

main()