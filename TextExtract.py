import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib
import string

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

    hash = hash%tableSize

    return hash

def retrieveIndex(word, hash):

    if(hTable[hash]==None):
        return -1
    elif(type(hTable[hash][0]) == list):
        for x in hTable[hash]:
            if(x[0]==word):
                return x[1]
            elif(x[0] == word):
                return x[1]
    elif(hTable[0] == word ):
                return hTable[hash][1]

    return -1

def addIndex(word, index, hash):
    if( hTable[hash] == None ):
        hTable[hash] = [word, index]
    elif ( type(hTable[hash][0]) == list):
        hTable[hash].append([word, index])
    else:
        hTable[hash] = [hTable[hash], [word, index]]


#Need to remove symbols, urls and stop words
for x in Text.stripped_strings:
    x.translate(str.maketrans("","",string.punctuation))

    #Removes punctuations
    cleanStr = ""
    for c in x:
        if c in string.ascii_letters or c in " ":
            cleanStr = cleanStr + c

    for y in cleanStr.split():
        hash = getHash(y)
        index =retrieveIndex(y,hash)
        if(index == -1):
            wordList[wordCount] = [y,1]
            addIndex(y,wordCount,hash)
            wordCount+=1
        else:
            wordList[index][1]+=1

for x in wordList:
    print(x)


