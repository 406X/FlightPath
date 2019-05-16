#Issues: redundant API requests due to multithreading

import requests

tableSize = 100
hTable_Dist = [None] * tableSize
hTable_request = [None] * tableSize
API_KEY = ""
count = 0

def getDistance(source, dest):
    global count
    hash = getHash(source, dest)
    dist = retrieveDist(source,dest,hash)

    if( dist == -1):
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        response = requests.get(url + 'origins=' + source +'&destinations=' + dest +'&key=' + API_KEY)
        responseJson = response.json()
        distance = responseJson['rows'][0]['elements'][0]["distance"]["value"]

        if(retrieveDist(source,dest,hash)==-1):
            addDist(source, dest, distance, hash)

        dist = distance

    return dist

def getCoords( location ):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    response = requests.get(url + 'address=' + location +'&key=' + API_KEY)
    responseJson = response.json()
    coords = [ responseJson['results'][0]['geometry']['location']['lat'],responseJson['results'][0]['geometry']['location']['lng'] ]
    return coords

def getHash(input, input2):
    hash = 0

    count = 1
    for x in input:
        hash+=((count)**2)*(ord(x)%11)
        count+=1

    count = 1
    for x in input2:
        hash+=((count)**2)*(ord(x)%11)
        count+=1

    hash = hash%100

    return hash


def retrieveDist(source, dest, hash):

    if(hTable_Dist[hash]==None):
        return -1
    elif(type(hTable_Dist[hash][0]) == list):
        for x in hTable_Dist[hash]:
            if(x[0]==source and x[1]==dest):
                return x[2]
            elif(x[0] == dest and x[1] == source):
                return x[2]
    elif(hTable_Dist[hash][0] == source and hTable_Dist[hash][1] == dest):
                return hTable_Dist[hash][2]
    elif(hTable_Dist[hash][0] == dest and hTable_Dist[hash][1] == source):
                return hTable_Dist[hash][2]

    return -1

def addDist(source,dest,distance,hash):
    if( hTable_Dist[hash] == None ):
        hTable_Dist[hash] = [source, dest, distance]
    elif ( type(hTable_Dist[hash][0]) == list):
        hTable_Dist[hash].append([source,dest,distance])
    else:
        hTable_Dist[hash] = [hTable_Dist[hash], [source, dest, distance]]

def addRequest(source,dest,hash):
    if( hTable_request[hash] == None ):
        hTable_request[hash] = [source, dest]
    elif ( type(hTable_request[hash][0]) == list):
        hTable_request[hash].append([source,dest])
    else:
        hTable_request[hash] = [hTable_request[hash], [source, dest]]

def removeRequest(source,dest,hash):
    if( hTable_request[hash] == None ):
        hTable_request[hash] = [source, dest]
    elif ( type(hTable_request[hash][0]) == list):
        hTable_request[hash].append([source,dest])
    else:
        hTable_request[hash] = [hTable_request[hash], [source, dest]]

def getTable():
    return hTable_Dist