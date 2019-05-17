import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import html5lib

link1 = "https://www.textise.net/showText.aspx?strURL=http%3a%2f%2f"
link2 = "google.com"
link = link1 + link2
req = urllib.request.Request(link,headers ={'User-Agent': "Mozilla/5.0"})
text = urllib.request.urlopen(req)


Text = BeautifulSoup(text,'html5lib')
for script in Text(["script", "style"]):
    script.decompose()

for x in Text.stripped_strings:
    if(x!=" "):
        print(x)





tableSize = 10000
hTable = [None] * tableSize

def getHash(input):
    hash = 0

    count = 1
    for x in input:
        hash+=((count)**2)*(ord(x))
        count+=1

    hash = hash%10000

    return hash

