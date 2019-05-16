#Issues: redundant API requests due to multithreading

import requests
import threading
import geopy.distance
from threading import Thread

#Hashtables
tableSize = 100
hTable_Dist = [None] * tableSize
#List of distances between two cities
#hTable_Dist[hash][0] = source
#hTable_Dist[hash][1] = destination
#hTable_Dist[hash][2] = distance

hTable_Coords = [None] * tableSize
#List of locations and their coordinates
#hTable_Coords[hash][0] = location name
#hTable_Coords[hash][1] = location coords; e.g "[[84.23124],[23,52321]]

hTable_request = [None] * tableSize
#Not yet implemented

API_KEY = ""

def getDistance(source, dest):
    hash = getHash(source, dest)
    dist = retrieveDist(source,dest,hash)

    if( dist == -1):

        t1 = thread_getCoords(source)
        t1.start()

        t2 = thread_getCoords(dest)
        t2.start()

        coords_source = t1.join()
        coords_dest = t2.join()

        str_coords_source = str(coords_source[0])+","+ str(coords_source[1])
        str_coords_dest = str(coords_dest[0]) + "," + str(coords_dest[1])

        distance = geopy.distance.vincenty(str_coords_source, str_coords_dest).km

        if(retrieveDist(source,dest,hash)==-1):
            addDist(source, dest, distance, hash)

        dist = distance

    return dist

def getCoords(location):

    hash = getHash2(location)
    coords = retrieveCoords(location, hash)
    if (coords == -1):

        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        response = requests.get(url + 'address=' + location +'&key=' + API_KEY)
        responseJson = response.json()
        coords = [ responseJson['results'][0]['geometry']['location']['lat'],responseJson['results'][0]['geometry']['location']['lng'] ]

        if(retrieveCoords(location, hash)==-1):
            addCoords(location,coords,hash)

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

def getHash2(input):
    hash = 0

    count = 1
    for x in input:
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

def retrieveCoords(location, hash):

    if(hTable_Coords[hash]==None):
        return -1
    elif(type(hTable_Coords[hash][0]) == list):
        for x in hTable_Coords[hash]:
            if(x[0]==location):
                return x[1]
            elif(x[0] == location):
                return x[1]
    elif(hTable_Coords[0] == location ):
                return hTable_Coords[hash][1]

    return -1

def addDist(source,dest,distance,hash):
    if( hTable_Dist[hash] == None ):
        hTable_Dist[hash] = [source, dest, distance]
    elif ( type(hTable_Dist[hash][0]) == list):
        hTable_Dist[hash].append([source,dest,distance])
    else:
        hTable_Dist[hash] = [hTable_Dist[hash], [source, dest, distance]]

def addCoords(location,coords,hash):
    if( hTable_Dist[hash] == None ):
        hTable_Dist[hash] = [location, coords]
    elif ( type(hTable_Dist[hash][0]) == list):
        hTable_Dist[hash].append( [location, coords])
    else:
        hTable_Dist[hash] = [hTable_Dist[hash],  [location, coords]]

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

class thread_getCoords(threading.Thread):
    def __init__(self, location):
        threading.Thread.__init__(self)
        self.location = location
        self.coords = []
    def run(self):

        self.coords = getCoords(self.location)

    def join(self):
        Thread.join(self)
        return self.coords