import math

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def convert_to_integer(key):
    if is_integer(key):
        return int(key)
    else:
        raise ValueError

def validatePublicKey(n, m, publicKey, privateKey):
    # Convert values to integer
    try:
        privateKey = [convert_to_integer(x) for x in privateKey]
        publicKey = [convert_to_integer(x) for x in publicKey]
    except ValueError:
        return False

    # Check if public key is not empty
    if len(publicKey) == 0:
        return False
    
    if len(publicKey) != len(privateKey):
        return False
    
    # Check if public key consists of negative or 0 values
    for key in publicKey:
        if key <= 0:
            return False
    
    for i in range(len(privateKey)):
        result = n * privateKey[i]
        result = result % m
        if publicKey[i] != result:
            return False
    return True

def validatePrivateKey(n, m, publicKey, privateKey):
    # Convert values to integer
    try:
        privateKey = [convert_to_integer(x) for x in privateKey]
        publicKey = [convert_to_integer(x) for x in publicKey]
    except ValueError:
        return False
    
    # Check if private key is not empty
    if len(privateKey) == 0:
        return False

    # Check if the sum of the private key is smaller than
    if m <= sum(privateKey):
        return False
    
    # Check if all values in private key are positive
    for key in privateKey:
        if key < 0:
            return False

    # Check for duplicates in the private key
    seen = set()
    for key in privateKey:
        if key not in seen:
            seen.add(key)
        else:
            return False

    for key in privateKey:
        if key > m:
            return False

    # Check if the private key is increasing
    for i in range(len(privateKey)):
        if privateKey[i] < sum(privateKey[:i]):
            return False
     
    if math.gcd(m, n) > 1:
        return False

    return True

mn = input()
privateKey = input()
publicKey = input()

n, m = mn.split()[0], mn.split()[1]
m = int(m)
n = int(n)

publicKey = publicKey.split()
privateKey = privateKey.split()

publicKeyValidation = validatePublicKey(n, m, publicKey, privateKey)
privateKeyValidation = validatePrivateKey(n, m, publicKey, privateKey)

if not privateKeyValidation:
    print(-1)
elif not publicKeyValidation:
    print(0)
else:
    print(1)