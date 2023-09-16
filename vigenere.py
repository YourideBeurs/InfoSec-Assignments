def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    k = 0
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if k > len(key) - 1:
                k = 0

            plain_code = ord(plaintext[i].lower()) - 97
            key_code = ord(key[k].lower()) - 97
            shift = (plain_code + key_code) % 26

            current_char = chr(shift + 97)

            if plaintext[i].isupper():
                ciphertext += current_char.upper()
            else:
                ciphertext += current_char

            k += 1
        else:
            ciphertext += plaintext[i]
    return ciphertext


def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    k = 0
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if k > len(key) - 1:
                k = 0

            cipher_code = ord(ciphertext[i].lower()) - 97
            key_code = ord(key[k].lower()) - 97
            shift = (cipher_code - key_code) % 26

            current_char = chr(shift + 97)

            if ciphertext[i].isupper():
                plaintext += current_char.upper()
            else:
                plaintext += current_char
            k += 1
        else:
            plaintext += ciphertext[i]
    return plaintext


line = input()
parts = line.split(' ', 1)  # Split only once
read_command = parts[0]
read_key = parts[1]

read_plaintext = []
while True:
    try:
        line = input()
    except EOFError:
        break
    read_plaintext.append(line)

read_plaintext = '\n'.join(read_plaintext)

if read_command == "e":
    print(vigenere_encrypt(read_plaintext, read_key))
else:
    print(vigenere_decrypt(read_plaintext, read_key))
