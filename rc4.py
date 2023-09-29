import sys

def rc4_init(key: bytes) -> list:
    S = list(range(256))
    K = [key[i % len(key)] for i in range(256)]  # repeating the key to fill the K array

    j = 0
    for i in range(256):
        j = (j + S[i] + K[i]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def rc4_stream(S: list) -> int:
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]

def rc4_encrypt(key: bytes, data: bytes, drop: int = 256) -> bytes:  # setting drop default value to 256
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