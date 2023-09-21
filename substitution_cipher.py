import sys

def shiftText(shiftNumber: int, text: str):
    newText = ''
    
    for char in text:
        # check if the character is lowercase
        charCode = ord(char)
        if charCode >= 97 and charCode <= 122:
            letterCode = charCode - 97
            letterCode = (letterCode + shiftNumber) % 26
            letterCode = letterCode + 97
            newText += chr(letterCode)
        
        # check if the character is uppercase
        elif charCode >=65 and charCode <= 90:
            letterCode = charCode - 65
            letterCode = (letterCode + shiftNumber) % 26
            letterCode = letterCode + 65
            newText += chr(letterCode)
        else:
            newText += char
    return newText

def mapText(mapper: str, text: str, encryptDecrypt: str):
    newText = ''

    for char in text:
        # check if the character is lowercase

        charCode = ord(char)
        if charCode >= 97 and charCode <= 122:
            letterCode = charCode - 97
            if encryptDecrypt == 'e':
                newLetter = mapper[letterCode]
            else:
                newLetter = chr(mapper.index(chr(letterCode + 97)) + 97)
            newText += newLetter

        # check if the character is uppercase
        elif charCode >=65 and charCode <= 90:
            letterCode = charCode - 65
            if encryptDecrypt == 'e':
                newLetter = mapper[letterCode].upper()
            else:
                newLetter = chr(mapper.index(chr(letterCode + 97)) + 97).upper()
            newText += newLetter
        else:
            newText += char
    return newText

key = input()

read_plaintext = []

for line in sys.stdin:
    read_plaintext.append(line.strip('\n'))

text = '\n'.join(read_plaintext)

splittedKeys = key.split()

result = text
for i in range(0, len(splittedKeys), 2):
    
    if splittedKeys[i+1].isnumeric():
        if splittedKeys[i] == 'e':
            multiplier = 1
        else:
            multiplier = -1
        result = shiftText(int(splittedKeys[i+1]) * multiplier, result)    
    else:
        result = mapText(str(splittedKeys[i+1]), result, splittedKeys[i+1])

print(result)