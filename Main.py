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
numRoutes = 3
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
    global numRoutes
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

    num = input("How many routes do you want? : ")
    numRoutes = int(num)

def calculateSentimentScores(routes):

    for x in routes:
        pass


    return

print("Generating route...")

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
            score = TE.getSentiment(x[y])
            if(score>10):
                score = 10
            if(score<-10):
                score=-10
            totalSentimentScore += score
        x.append(totalSentimentScore)

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
t = Thread(TE.init2(cities))
t.start()


routes = RT.getAllRoutes(source, dest)
Thread2 = []

t.join()
for x in routes:
    t = thread_Thread(x)
    t.start()
    Thread2.append(t)

for r in Thread2:
    r.join()

length = len(routes[0])-2
routes = RT.quickSort( routes, 0 , len(routes)-1, val = length )

lengthRoutes = len(routes)
if(numRoutes>len(routes)):
    print("## Requested " + str(numRoutes) + " routes but only " + str(lengthRoutes) +" Available." )

#Probability calculation based on distance alone
totalDist = 0.0
for x in range(numRoutes):
    if(x > lengthRoutes-1):
        break
    totalDist += routes[x][length]

totalWeight=0.0
for x in range(numRoutes):
    if(x > lengthRoutes-1):
        break
    totalWeight += 1/(routes[x][length]/totalDist)

for x in range(numRoutes):
    if(x > lengthRoutes-1):
        break
    print(str(x+1) + ". Route: " + str(routes[x][0:numTransits]) + " | Distance: {:0.5f}KM".format(routes[x][length]) +" | Sentiment Score: " + str(routes[x][length+1]) +" | Probability: {:0.5f}".format((1/(routes[x][length]/totalDist)/(totalWeight/100))) +"%" )


end = time.time()
print("Time: "+ str(end - startTime))

numChoice = 0
while(1==1):
    num = input("Which route would you like to display? (1-"+ str(numRoutes)+"): ")
    if(int(num) <= 0 or int(num)>numRoutes):
        print("Invalid number")
        continue
    else:
        numChoice = int(num)-1
        chosenRoute = []

        for x in routes[numChoice]:
            if (type(x) == float):
                break
            chosenRoute.append(x)
        showRoute(chosenRoute)

    choice ='Y'
    while(1==1):
        choice = input("Do you want to diplay another route?(Y/N): ")
        if (choice == "Y" or choice == "y"):
            break
        elif (choice == "N" or choice == "n"):
            print("Ending Program...")
            break
        else:
            print("Invalid Option")
            continue

    if (choice == "N" or choice == "n"):
        break




