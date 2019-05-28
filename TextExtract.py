import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import string
import re

link1 = "https://www.textise.net/showText.aspx?strURL=http%3a%2f%2f"
link2 = "google.com"
link = link1 + link2
req = urllib.request.Request(link,headers ={'User-Agent': "Mozilla/5.0"})
text = urllib.request.urlopen(req)

Text = BeautifulSoup(text,'html5lib')
for script in Text(["script", "style"]):
    script.decompose()


tableSize = 10000
wordList = [None] * tableSize
hTable = [None] * tableSize
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

def addIndex(word, index, hash):
    if( hTable[hash] == None ):
        hTable[hash] = [word, index]
    elif ( type(hTable[hash][0]) == list):
        hTable[hash].append([word, index])
    else:
        hTable[hash] = [ hTable[hash], [word, index] ]


def string_removeURL(input):
    input = re.sub("www.[\w]", "", input)
    input = re.sub("[\w]+.net", "", input)
    input = re.sub("[\w]+.org", "", input)
    input = re.sub("[\w]+.com", "", input)
    return re.sub("http[^\s]+", "", input)

def string_removePunctuation(input):
    cleanStr = ""

    for c in input:
        if c in string.ascii_letters or c in " ":
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

stops = open("stopword.txt", encoding='utf-8')
stopList = []

for c in stops:
    stopList.append(c.strip())

for x in Text.stripped_strings:

    cleanStr = x
    cleanStr = string_removeURL(cleanStr)
    cleanStr = string_removeInList(cleanStr, stopList)
    cleanStr = string_removePunctuation(cleanStr)
    cleanStr = string_normalize(cleanStr)

    if(cleanStr!=''):
        for y in cleanStr.split():
            hash = getHash(y)

            index =retrieveIndex(y,hash)

            if(index == -1):
                wordList[wordCount] = [y,1]
                addIndex(y,wordCount,hash)
                wordCount+=1
            else:
                wordList[index][1]+=1

for x in range(wordCount):
    print(wordList[x])


