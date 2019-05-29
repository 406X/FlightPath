import re
import string

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

