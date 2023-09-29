
def encrypt_message(inputNumber, publicKey):
    cipherText = 0
    for i in range(len(publicKey)):
        if (inputNumber >> i) & 1:
            cipherText += publicKey[i]
    return cipherText

def decrypt_message(cipherText, privateKey):
    modular_inverse = pow(privateKey[-1], -1, privateKey[-2])

    plaintext = 0

    for i in range(len(privateKey) -1):
        plaintext += (cipherText * modular_inverse * privateKey[i]) % privateKey[-2]
    
    return plaintext

def validatePublicKey(n, m, publicKey, privateKey):
    for i in range(len(privateKey)):
        result = n * privateKey[i]
        result = result % m
        if publicKey[i] != result:
            return -1
    return 1

def validatePrivateKey(n, m, publicKey, privateKey):
    inputNumber = 100
    cipherText = encrypt_message(inputNumber, publicKey)
    result = decrypt_message(cipherText, privateKey)

    if inputNumber != result:
        return -1
    return 1

mn = input()
m, n = mn.split()[0], mn.split()[1]
m = int(m)
n = int(n)

privateKey = input().split()
publicKey = input().split()
privateKey = [int(x) for x in privateKey]
publicKey = [int(x) for x in publicKey]

publicKeyValidation = validatePublicKey(n, m, publicKey, privateKey)
privateKeyValidation = validatePrivateKey(n, m, publicKey, privateKey)

if publicKeyValidation == -1 or privateKeyValidation == -1:
    print(-1)
else:
    print(1)