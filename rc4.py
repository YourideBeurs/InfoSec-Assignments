import sys

def rc4_init(key: bytes) -> list:
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_stream(S: list) -> int:
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]

def rc4_encrypt(key: bytes, data: bytes, drop: int = 3072) -> bytes:
    S = rc4_init(key)
    stream = rc4_stream(S)

    # Drop initial bytes
    for _ in range(drop):
        next(stream)

    return bytes([x ^ next(stream) for x in data])

def main():
    content = sys.stdin.buffer.read()
    key, _, data = content.partition(b'\xFF')

    encrypted_data = rc4_encrypt(key, data)
    sys.stdout.buffer.write(encrypted_data)

main()