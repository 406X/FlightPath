import Location as lc
import webbrowser
import os
import RouteV3 as RT
import TextExtract as TE
from mako.template import Template
import time
import threading
from threading import Thread
import plotly.offline as py
import plotly.graph_objs as go

cities = { "Beijing","Dubai","Los Angeles","Tokyo","London","Hong Kong","Amsterdam","Incheon","Istanbul","Singapore","Argentina","Delhi","Madrid","Kuala Lumpur","Bangkok","Ho Chi Minh City",}

#Yes don't steal this >.>
API_KEY = "AIzaSyAn27el7Uuj1qLQvpZgF9fbVjGLu_HPhbQ"
plotlykey ="dtu6qHyNFsVF1wQSWWhS"
# Google Cloud API Key
# This program uses the following Google Cloud APIs
# - Geocoding API
# - Maps JavaScript API


def showRoute(route, source , dest):

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
    numTransits = 3
    numRoutes = 3
    source = "Kuala Lumpur"
    dest = "dasdsa"
    list = cities.copy()
    print("Source: "+ source)
    #print("Enter a starting location:")
    #print("Available options:")
    #for c in list:
    #    print(" -" + c)
    #source = input("Input: ")
    list.remove(source)

    while(dest not in cities):
        print("Enter destination location:")
        print("Available options:")
        for c in list:
            print(" -" + c)

        dest = input("Input: ")
        if(dest not in cities):
            print("Invalid Input")
            continue

    list.remove(dest)


    limit = 5
    num = -1
    while(int(num)<=0 or int(num) >limit):
        num = input("Number of transits to make (1-" + str(limit) + ") : ")

        if(int(num)<=0 or int(num) >limit):
            print("Invalid Input")

    numTransits = int(num)

    num2 = -1
    while(int(num2)<=0):
        num2 = input("How many routes do you want? : ")

        if(int(num2)<=0):
            print("Value cannot be less than 1")

    numRoutes = int(num2)

    print("Generating route...")
    startTime = time.time()

    # Init
    RT.cities = cities
    RT.dest = dest
    RT.minTransits = numTransits
    lc.API_KEY = API_KEY
    TE.init()
    t = Thread(TE.init2(cities))
    t.start()

    routes = RT.getAllRoutes(source, dest)
    t.join()


    Thread2 = []
    for x in routes:
        t = thread_Thread(x)
        t.start()
        Thread2.append(t)

    for r in Thread2:
        r.join()

    length = len(routes[0]) - 2
    routes = RT.quickSort(routes, 0, len(routes) - 1, val=length)

    lengthRoutes = len(routes)
    if (numRoutes > len(routes)):
        print("## Requested " + str(numRoutes) + " routes but only " + str(lengthRoutes) + " Available.")
        numRoutes = len(routes)

    # Probability calculation based on distance alone
    totalDist = 0.0
    for x in range(numRoutes):
        if (x > lengthRoutes - 1):
            break
        totalDist += routes[x][length]

    totalWeight = 0.0
    for x in range(numRoutes):
        if (x > lengthRoutes - 1):
            break
        totalWeight += 1 / (routes[x][length] / totalDist)

    for x in range(numRoutes):
        if (x > lengthRoutes - 1):
            break
        print(str(x + 1) + ". Route: " + str(routes[x][0:numTransits]) + " | Distance: {:0.5f}KM".format(
            routes[x][length]) + " | Sentiment Score: " + str(routes[x][length + 1]) + " | Probability: {:0.5f}".format(
            (1 / (routes[x][length] / totalDist) / (totalWeight / 100))) + "%")

    end = time.time()
    print("Time: " + str(end - startTime))

    while (1 == 1):
        choice = input("Would you like to display Plotly charts on mined data?(Y/N): ")
        if (choice == "Y" or choice == "y"):
            list1 = TE.getStopList()
            plotBar(list1, name="Stops.html")
            list2 = TE.getWordList()
            plotBar(list2, name="Words.html")
            list3 = TE.getPositiveList()
            plotBar(list3, name="Positive.html")
            list4 = TE.getNegativeList()
            plotBar(list4, name="Negative.html")
            break
        elif (choice == "N" or choice == "n"):
            break
        else:
            print("Invalid Option")
            continue

    numChoice = 0
    while (1 == 1):
        num = input("Which route would you like to display? (1-" + str(numRoutes) + "): ")
        if (int(num) <= 0 or int(num) > numRoutes):
            print("Invalid number")
            continue
        else:
            numChoice = int(num) - 1
            chosenRoute = []

            for x in routes[numChoice]:
                if (type(x) == float):
                    break
                chosenRoute.append(x)
            showRoute(chosenRoute, source, dest)

        choice = 'Y'
        while (1 == 1):
            choice = input("Do you want to display another route?(Y/N): ")
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




class thread_Thread(threading.Thread):
    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x

    def run(self):
        totalSentimentScore = 0
        Thread3 = []
        length = len(self.x)
        for y in range(length):
            if (type(self.x[y]) == float):
                continue
            t = ThreadWithReturnValue(target=TE.getSentiment,args=self.x[y])
            t.start()
            Thread3.append(t)

        for x in Thread3:
            score = x.join()
            if (score > 10):
                score = 10
            if (score < -10):
                score = -10
            totalSentimentScore += score

        self.x.append(totalSentimentScore)

def join(self):
    Thread.join(self)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), Verbose=None):
        Thread.__init__(self, group, target, name, args)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(self._args)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def plotBar(input, name=("Plot.html")):

    x1 = []
    y1 = []
    for x in input:
        x1.append(x[0])
        y1.append(x[1])

    trace = go.Bar( x=x1,y=y1)
    data = [trace]

    py.plot(data,filename=(name))


def plotHistogram(input, name=("Plot.html")):
    x1 = []
    for x in input:
        if (x == None):
            return
            x1.append(x[0])

    trace = go.Histogram(x1)
    data = [trace]

    py.plot(data, filename=(name))

start()
