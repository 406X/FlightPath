import Location as lc
import webbrowser
import os
import RouteV3 as RT
import TextExtract as TE
from mako.template import Template
import time
import threading
from threading import Thread

#Variables
numTransits = 3
source = "Kuala Lumpur"
dest= "Dubai"
cities = { "Beijing","Dubai","Los Angeles","Tokyo","London","Hong Kong","Amsterdam","Incheon","Istanbul","Singapore","Argentina","Delhi","Madrid","Kuala Lumpur"}

API_KEY = "AIzaSyAn27el7Uuj1qLQvpZgF9fbVjGLu_HPhbQ"
# Google Cloud API Key
# This program uses the following Google Cloud APIs
# - Geocoding API
# - Maps JavaScript API


def showRoute(route):

    coords = []

    coords.append(lc.getCoords(source))
    for x in route:
        coords.append(lc.getCoords(x))
    coords.append(lc.getCoords(dest))

    lat = []
    lng = []
    count = 0
    for x in coords:
        lat.append(coords[count][0])
        lng.append(coords[count][1])
        count+=1


    pageTemplate = open("poly.html").read()
    pageTemplate = Template(pageTemplate).render(x_APIKEY = API_KEY, x_lat=lat, x_lng=lng, x_size=count)

    routePage = open("route.html", "w+")
    routePage.write(pageTemplate)
    routePage.close()

    webbrowser.open('file://' + os.path.realpath("route.html"));

def start():
    global dest
    #global source
    global numTransits
    list = cities.copy()
    print("Source: "+ source)
    #print("Enter a starting location:")
    #print("Available options:")
    #for c in list:
    #    print(" -" + c)
    #source = input("Input: ")
    list.remove(source)

    print("Enter destination location:")
    print("Available options:")
    for c in list:
        print(" -" + c)
    dest = input("Input: ")
    list.remove(dest)
    num = input("Number of transits to make (1-5) : ")
    numTransits = int(num)

def calculateSentimentScores(routes):

    for x in routes:
        pass


    return

print("Generating route...")

#For easy multithreading with return values
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=()):
        Thread.__init__(self, group, target, name, args)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(self._args)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

class thread_Thread(threading.Thread):
    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x

    def run(self):
        totalSentimentScore = 0
        Thread3 = []
        length = len(self.x)
        for y in range(length):
            if (type(x[y]) == float):
                continue
            t = ThreadWithReturnValue( target=TE.getSentiment, args=(self.x[y]) )
            t.start()
            Thread3.append(t)

        for r in Thread3:
            totalSentimentScore += r.join()

        self.x.append(totalSentimentScore)


    def join(self):
        Thread.join(self)

start()

startTime = time.time()

#Init
RT.cities = cities
RT.dest = dest
RT.minTransits = numTransits
lc.API_KEY = API_KEY
TE.init()


routes = RT.getAllRoutes(source, dest)
Thread2 = []

for x in routes:
    t = thread_Thread(x)
    t.start()
    Thread2.append(t)

for r in Thread2:
    r.join()

for x in routes:
    print(x)

end = time.time()
print("Time:")
print(end - startTime)

#showRoute(route)

