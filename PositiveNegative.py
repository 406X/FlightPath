import stringFuncs as SF

tableSize = 1000

positiveList = []
negativeList = []
hTablePositiveList = [None] * tableSize
hTableNegativeList = [None] * tableSize
positiveCount = 0
negativeCount = 0


def init():
    global  hTablePositiveList
    global  hTableNegativeList
    positive  = open("positive-words.txt",encoding='utf-8')
    for c in positive:
        d = c.strip()
        d = SF.string_removePunctuation(d)
        d = SF.string_normalize(d)
        hash = getHash(d)
        addData(d, hash, hTablePositiveList)

    negative = open("negative-words.txt",encoding='utf-8')
    for c in negative:
        d = c.strip()
        d = SF.string_removePunctuation(d)
        d = SF.string_normalize(d)
        hash = getHash(d)
        addData(d,hash,hTableNegativeList)

def getHash(input):
    hash = 0

    count = 1
    for x in input:
        hash+=((count)**2)*(ord(x))
        count+=1

    hash = hash % tableSize

    return hash


def addData(word, hash, hTable):
    if (hTable[hash] == None):
        hTable[hash] = word
    elif (type(hTable[hash][0]) == list):
        hTable[hash].append(word)
    else:
        hTable[hash] = [hTable[hash], word]

def inTable(word, hash, hTable):
    if(hTable[hash] == None):
        return -1
    elif( type( hTable[hash] ) == list):
        for x in hTable[hash]:
            if(x == word):
                return 1
            elif(x == word):
                return 1
    elif(hTable[hash] == word ):
            return 1
    return -1


def inPositiveList(input):
    global hTablePositiveList
    hash = getHash(input)
    return inTable(input, hash,hTablePositiveList)

def inNegativeList(input):
    global hTableNegativeList
    hash = getHash(input)
    return inTable(input, hash, hTableNegativeList)