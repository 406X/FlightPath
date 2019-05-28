import string
import re
import json
import requests

tableSize = 2000
wordList = [None]
hTable = [None] * tableSize
hTableSentiment = [None] * tableSize
positiveList = []
negativeList = []
stopList = []
wordCount = 0

def getHash(input):
    hash = 0

    count = 1
    for x in input:
        hash+=((count)**2)*(ord(x))
        count+=1

    hash = hash % tableSize

    return hash

def retrieveIndex(word, hash):
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

def retrieveSentiment(country, hash):

    if(hTableSentiment[hash] == None):
        return -1
    elif( type( hTableSentiment[hash][0] ) == list):
        for x in hTableSentiment[hash]:
            if(x[0] == country):
                return x[1]
            elif(x[0] == country):
                return x[1]
    elif(hTableSentiment[hash][0] == country):
            return hTableSentiment[hash][1]
    return -1

def addIndex(word, index, hash):
    global hTable
    if( hTable[hash] == None ):
        hTable[hash] = [word, index]
    elif ( type(hTable[hash][0]) == list):
        hTable[hash].append([word, index])
    else:
        hTable[hash] = [ hTable[hash], [word, index] ]

def addSentiment(country, score, hash):
    global hTableSentiment
    if( hTableSentiment[hash] == None ):
        hTableSentiment[hash] = [country, score]
    elif ( type(hTableSentiment[hash][0]) == list):
        hTableSentiment[hash].append([country, score])
    else:
        hTableSentiment[hash] = [hTableSentiment[hash], [country, score]]

def string_removeURL(input):
    input = re.sub("www.[\w]", "", input)
    input = re.sub("[\w]+.net", "", input)
    input = re.sub("[\w]+.org", "", input)
    input = re.sub("[\w]+.com", "", input)
    return re.sub("http[^\s]+", "", input)

def string_removePunctuation(input):
    cleanStr = ""

    for c in input:
        if c in string.ascii_letters or c in " " :
            cleanStr = cleanStr + c

    return cleanStr

def string_removeInList(input, list):
    cleanStr=''
    for c in input.split():
        if(c.lower() not in list):
            cleanStr = cleanStr + " " + c

    return cleanStr

def string_normalize(input):
    cleanStr = input.lower()
    return cleanStr

def getTokens(input):
    global wordList
    global wordCount
    country = input

    newsResponse = requests.get("https://newsapi.org/v2/everything?q="+country+"&apiKey=e55e396153fe47d4a405dca429297f97")
    newStr = json.dumps(newsResponse.json())

    #Counts how many words in list

    for x in newStr.split():
        cleanStr = x
        cleanStr = string_removeURL(cleanStr)
        cleanStr = string_removeInList(cleanStr, stopList)
        cleanStr = string_removePunctuation(cleanStr)
        cleanStr = string_normalize(cleanStr)

        if (cleanStr != ''):
            for y in cleanStr.split():
                hash = getHash(y)

                index = retrieveIndex(y, hash)
                if (index == -1):
                    if(wordCount == 0):
                        wordList = [[y,1]]
                    else:
                        wordList.append( [y, 1] )

                    addIndex(y, wordCount, hash)
                    wordCount += 1

                else:
                    wordList[index][1] += 1

    return wordList

def init():
    stops = open("stopword.txt", encoding='utf-8')
    for c in stops:
        d = c.strip()
        d = string_removePunctuation(d)
        d = string_normalize(d)
        stopList.append(d)

    positive = stops = open("positive-words.txt")
    for c in positive:
        d = c.strip()
        d = string_removePunctuation(d)
        d = string_normalize(d)
        positiveList.append(d)

    negative = stops = open("negative-words.txt")
    for c in negative:
        d = c.strip()
        d = string_removePunctuation(d)
        d = string_normalize(d)
        negativeList.append(d)

def getSentiment(input):
    pointsPositive = 0
    pointsNegative = 0

    hash = getHash(input)
    score = retrieveSentiment(input, hash)
    if (score != -1):
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
            if(words[x] in positiveList):
                pointsPositive += frequency[x]

            elif(words[x] in negativeList):
                pointsNegative += frequency[x]

        score = pointsPositive - pointsNegative
        addSentiment(input,score,hash)

    return score

