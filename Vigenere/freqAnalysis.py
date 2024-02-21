from functools import cmp_to_key

englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99,
                     'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
                     'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def getLetterCount(message):
    letterCount = [0 for _ in range(len(LETTERS))]
    # Returns a list count of how many times 'A'-'Z' appear in the message parameter.
    for letter in message.upper():
        letterId = LETTERS.find(letter)
        if letterId != -1:
            letterCount[letterId] += 1
    return letterCount


def getFrequencyOrder(message):
    # Returns a string of the alphabet letters arranged in order of most

    # first count letter frequency
    letterCount = getLetterCount(message)

    # sort letter by frequency
    listLetterFreqs = []
    for i in range(len(LETTERS)):
        listLetterFreqs.append((LETTERS[i], letterCount[i]))
    listLetterFreqs.sort(key=lambda letterFreq: letterFreq[1], reverse=True)

    # extract all the letters for the final string
    freqOrder = []
    for letterFreq in listLetterFreqs:
        freqOrder.append(letterFreq[0])
    return ''.join(freqOrder)


def englishFreqMatchScore(message):
    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters is among the six most frequent and
    # six least frequent letters for English.
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # Find how many matches for the six most common letters there are.
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # Find how many matches for the six least common letters there are.
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore
