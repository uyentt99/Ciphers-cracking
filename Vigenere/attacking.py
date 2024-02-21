import itertools, re
import math

import vigenereCipher, pyperclip, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SILENT_MODE = False  # if set to True, program doesn't print attempts
STOP = True
MAX_KEY_LENGTH = 16  # will not attempt keys longer than this
MIN_NUM_MOST_FREQ_LETTERS = 4  # attempts this many letters per subkey
NONLETTERS_PATTERN = re.compile('[^A-Z]')


def main():
    file2 = open('input2.inp')
    cipherText = file2.read()
    hackedMessage = hackVigenere(cipherText)

    if hackedMessage is not None:
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
        print('The message has been copied to the clipboard.')
    else:
        print('Failed to hack encryption.')


def findRepeatSequencesSpacings(message):
    # Goes through the message and finds any 3 to 5 letter sequences
    # that are repeated. Returns a list of spacings

    # Use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('', message.upper())

    # Compile a list of seqLen-letter sequences found in the message.
    seqSpacings = []
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = message[seqStart:seqStart + seqLen]

            # Look for this sequence in the rest of the message
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings.append(i - seqStart)
    return seqSpacings


def getUsefulFactors(num):
    # Returns a list of useful factors of num. B
    if num < 2:
        return []
    factors = []  # the list of factors found
    for i in range(2, min(MAX_KEY_LENGTH, int(math.sqrt(num))) + 1):
        if num % i == 0:
            factors.append(i)
            if i * i != num:
                j = int(num / i)
                if j <= MAX_KEY_LENGTH:
                    factors.append(j)
    if num <= MAX_KEY_LENGTH:
        factors.append(num)

    return factors


def getMostCommonFactors(seqFactors):
    # get a count of how many times a factor occurs in seqFactors.
    factorCounts = {}  # key is a factor, value is how often if occurs

    for factorList in seqFactors:
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them.
    factorsByCount = []
    for factor in factorCounts:
        if factor<=MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorCounts[factor]))
    # sort by count
    factorsByCount.sort(key=lambda x: x[1], reverse=True)
    return factorsByCount


def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times

    # Find spacing of repeated sequences
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)

    # get all factor of spacing
    spaceFactors = []
    for spacing in repeatedSeqSpacings:
        spaceFactors.append(getUsefulFactors(spacing))

    # See getMostCommonFactors() for a description of factorsByCount.
    factorsByCount = getMostCommonFactors(spaceFactors)

    # Now we extract the factor from factorsByCount and
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths


def getNthSubkeysLetters(n, keyLength, message):
    # Returns every Nth letter for each keyLength set of letters in text.

    # Use a regular expression to remove non-letters from the message.
    message = NONLETTERS_PATTERN.sub('', message)

    letters = []
    for i in range(n, len(message), keyLength):
        letters.append(message[i])

    return ''.join(letters)


def getNextCombine(indexes, allFreqKey):
    n = len(indexes)
    j = n - 1
    while j >= 0 and indexes[j] + 1 == len(allFreqKey[j]):
        j -= 1
    if j == -1:
        return None
    indexes[j] += 1
    for i in range(j + 1, n):
        indexes[i] = 0
    return indexes


def attemptHackWithKeyLength(cipherText, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key.
    cipherTextUp = cipherText.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    allFreqKey = []
    for nth in range(mostLikelyKeyLength):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, cipherTextUp)

        # freqScores is a list of tuples like:
        # [(<letter>, <Eng. Freq. match score>), ... ]
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            matchScore = freqAnalysis.englishFreqMatchScore(decryptedText)
            freqScores.append((possibleKey, matchScore))
        # Sort by match score
        freqScores.sort(key=lambda x: x[1], reverse=True)
        # Get top letter
        numFreq = MIN_NUM_MOST_FREQ_LETTERS
        while numFreq < len(LETTERS) and freqScores[0][1] == freqScores[numFreq][1]:
            numFreq += 1
        freqKey = [fs[0] for fs in freqScores[:numFreq]]
        allFreqKey.append(freqKey)

    if not SILENT_MODE:
        for i in range(mostLikelyKeyLength):
            print('Possible letters for letter %s of the key: ' % (i + 1) + getStringPrint(allFreqKey[i]))

    # Try every combination of the most likely letters for each position
    # in the key.
    indexes = [0 for _ in range(mostLikelyKeyLength)]
    while indexes is not None:
        # Create a possible key
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqKey[i][indexes[i]]

        if not SILENT_MODE:
            print('Attempting with key: %s' % possibleKey)

        decryptedText = vigenereCipher.decryptMessage(possibleKey, cipherTextUp)

        if detectEnglish.isEnglish(decryptedText):
            # Set the hacked ciphertext to the original casing.
            origCase = []
            for i in range(len(cipherText)):
                if cipherText[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            # Check with user to see if the key has been found.
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])  # only show first 200 characters
            print()
            if STOP:
                print('Enter D for done, or just press Enter to continue hacking:')
                response = input('> ')
                if response.strip().upper().startswith('D'):
                    return decryptedText

        indexes = getNextCombine(indexes, allFreqKey)
    # No English-looking decryption found, so return None.
    return None


def hackVigenere(ciphertext):
    hackedMessage = None
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is.
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        print('Kasiski Examination results say the most likely key lengths are: ' + getStringPrint(allLikelyKeyLengths))

    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('\nAttempting hack with key length %s' % keyLength)
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage is not None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths.
    if hackedMessage is None:
        if not SILENT_MODE:
            print('\nUnable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH+1):
            # don't re-check key lengths already tried from Kasiski
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('\nAttempting hack with key length %s...' % keyLength)
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage is not None:
                    break
    return hackedMessage


def getStringPrint(listA):
    s = ''
    for x in listA:
        s += '%s ' % x
    return s


# the main() function.
if __name__ == '__main__':
    main()
