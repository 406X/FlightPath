import json
import requests
from threading import Thread,Lock
import stringFuncs as SF
import PositiveNegative as PN

tableSize = 1000
hTableSentiment = [None] * tableSize
foundPositive = [None]
foundNegative = [None]
stopList = []
foundStops = [None]
#API_KEY = "700b3d57bcdf4813b66949f4460dc591"
API_KEY = "e55e396153fe47d4a405dca429297f97"
#API_KEY = "6f1f74565b754b70a1c55f33310e6378"
wordCount = 0
stopCount = 0
positiveCount = 0
negativeCount = 0
wordList = [None]
hTable = [None] * tableSize
hTablePositive = [None] * tableSize
hTableNegative = [None] * tableSize
hTableStops = [None] * tableSize

def getHash(input):
    hash = 0

    count = 1
    for x in input:
        hash+=((count)**2)*(ord(x))
        count+=1

    hash = hash % tableSize

    return hash

def retrieveIndex(word, hash, hTable):
    if(hTable[hash] == None):
        return -1
    elif( type( hTable[hash][0] ) == list):
        for x in hTable[hash]:
            if(x[0] == word):
                return x[1]
            elif(x[0] == word):
                return x[1]
    elif(hTable[hash][0] == word ):
            return hTable[hash][1]
    return -1

def retrieveSentiment(city, hash):
    if(hTableSentiment[hash] == None):
        return None
    elif( type( hTableSentiment[hash][0] ) == list):
        for x in hTableSentiment[hash]:
            if(x[0] == city):
                return x[1]
    elif(hTableSentiment[hash][0] == city):
            return hTableSentiment[hash][1]

def addIndex(word, index, hash,hTable):
    if( hTable[hash] == None ):
        hTable[hash] = [word, index]
    elif ( type(hTable[hash][0]) == list):
        hTable[hash].append([word, index])
    else:
        hTable[hash] = [ hTable[hash], [word, index] ]

def addSentiment(city, score, hash):
    global hTableSentiment
    if( hTableSentiment[hash] == None ):
        hTableSentiment[hash] = [city, score]
    elif ( type(hTableSentiment[hash][0]) == list):
        hTableSentiment[hash].append([city, score])
    else:
        hTableSentiment[hash] = [hTableSentiment[hash], [city, score]]


def search(pat, txt, q=101):
    d = 256
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1

    if(N!=M):
        return -1

    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break

            j += 1
            if j == M:
                return 1

        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q

            if t < 0:
                t = t + q

    return -1

def getTokens(input):
    global wordCount
    global wordList
    global hTable
    global hTableStops
    global foundStops
    global stopCount
    local_wordList = [None]
    local_hTable = [None]*tableSize
    local_wordCount = 0

    city = input
    newsResponse = requests.get("https://newsapi.org/v2/everything?q="+city+"&apiKey="+API_KEY)
    newStr = json.dumps(newsResponse.json())

    #Counts how many words in list
    lock = Lock()
    for x in newStr.split():
        cleanStr = x
        cleanStr = SF.string_removeURL(cleanStr)
        cleanStr = SF.string_removePunctuation(cleanStr)
        cleanStr = SF.string_normalize(cleanStr)

        lock = Lock()

        for c in stopList:

            found = search(cleanStr, c)

            if (found == 1):
                hash = getHash(cleanStr)

                index = retrieveIndex(cleanStr, hash, hTableStops)
                if (index == -1):
                    addIndex(cleanStr, stopCount, hash, hTableStops)
                    if (stopCount == 0):
                        foundStops = [[cleanStr, 1]]
                    else:
                        foundStops.append([cleanStr, 1])
                    stopCount += 1

                else:
                    foundStops[index][1] += 1
                cleanStr=''

        if (cleanStr != ''):

            y = cleanStr
            hash = getHash(y)
            index = retrieveIndex(y,hash, hTable)
            local_index = retrieveIndex(y, hash, local_hTable)

            if (index == -1 or local_index == -1):

                #Add to local wordlist
                addIndex(y, local_wordCount, hash, local_hTable)
                if (local_wordCount == 0):
                    local_wordList = [[y, 1]]
                else:
                    local_wordList.append([y, 1])
                local_wordCount += 1

                # Add to global wordlist
                lock.acquire()
                addIndex(y, wordCount, hash, hTable)

                if (wordCount == 0):
                    wordList = [[y, 1]]
                else:
                    wordList.append([y, 1])


                wordCount += 1
                lock.release()

            else:
                local_wordList[local_index][1] += 1
                lock.acquire()
                wordList[index][1] += 1
                lock.release()



    return local_wordList

def init():
    stops = open("stopword.txt", encoding='utf-8')
    for c in stops:
        d = c.strip()
        d = SF.string_removePunctuation(d)
        d = SF.string_normalize(d)
        stopList.append(d)

    PN.init()

class simpleThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), Verbose=None):
        Thread.__init__(self, group, target, name, args)

    def run(self):
        self._target(self._args)

    def join(self, *args):
        Thread.join(self, *args)


def init2(cities):
    threads = []
    for x in cities:
        t = simpleThread(target=getSentiment, args=x)
        t.start()
        threads.append(t)

    for x in threads:
        x.join()


def getSentiment(input):
    global positiveCount
    global negativeCount
    global foundNegative
    global foundPositive
    global hTableNegative
    global hTablePositive
    global hTableSentiment

    pointsPositive = 0
    pointsNegative = 0

    hash = getHash(input)
    score = retrieveSentiment(input, hash)
    if (score != None):
        return score
    else:
        tokens = getTokens(input)
        words = []
        frequency = []
        for x in tokens:
            words.append(x[0])
            frequency.append(x[1])

        length = len(words)
        for x in range(length):

            hash2 = getHash(words[x])
            if(PN.inPositiveList(words[x]) == 1):

                addIndex(words[x], positiveCount, hash2, hTablePositive)

                if (positiveCount == 0):
                    foundPositive = [[words[x], frequency[x]]]
                else:
                    foundPositive.append([words[x], frequency[x]])

                positiveCount += 1

                pointsPositive += frequency[x]

            elif(PN.inNegativeList(words[x]) == 1):
                addIndex(words[x], negativeCount, hash2, hTableNegative)

                if (negativeCount == 0):
                    foundNegative = [[words[x], frequency[x]]]
                else:
                    foundNegative.append([words[x], frequency[x]])

                negativeCount += 1

                pointsNegative += frequency[x]

        score = pointsPositive - pointsNegative

        addSentiment(input,score,hash)

    return score


def getWordList():
    return wordList

def getPositiveList():
    return foundPositive

def getNegativeList():
    return foundNegative

def getStopList():
    return foundStops