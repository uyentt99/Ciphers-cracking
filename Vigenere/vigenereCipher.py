import pyperclip

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    file1 = open('input.inp')
    myMode = int(file1.readline())
    myKey = file1.readline().replace('\n', '')
    myMessage = file1.read()

    if myMode == 1:
        translated = encryptMessage(myKey, myMessage)
    else:
        translated = decryptMessage(myKey, myMessage)
    pyperclip.copy(translated)
    print(translated)
    print()
    print('The message has been copied to the clipboard.')


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = []

    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not found in LETTERS
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex])  # add if encrypting
            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex])  # subtract if decrypting

            num %= len(LETTERS)  # handle the potential wrap-around

            # add the encrypted/decrypted symbol to the end of translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1  # move to the next letter in the key
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)

    return ''.join(translated)


# the main() function.
if __name__ == '__main__':
    main()
