import Location as lc
from copy import deepcopy
import threading
from threading import Thread

#Version 3
# Changes:
# -Each search depth level is now its own thread(multi-threading) (Much faster)

cities = []
minTransits = 0
dest = ""
bestcost = -1

def getAllRoutes(source,desti):
    dest = desti
    transit = cities
    transit.remove(source)
    transit.remove(dest)
    toTransit = []
    allRoutes = []
    # Depth of search algo
    # for best result use searchDepth = minTransits
    # Exponentially increases search time
    searchDepth = minTransits

    # Width of search algo
    # defines how many cities should be considered as transit at each depth level
    searchWidth = 3  # len(cities)

    currTransits = 0
    current = source

    while (currTransits < minTransits):

        toTransit.extend(bestRoute(current, transit, searchDepth, searchWidth, currTransits, allRoutes))

        currTransits = len(toTransit)
        for t in toTransit:
            try:
                transit.remove(t)
            except KeyError:
                pass

        current = toTransit[len(toTransit) - 1]

    #print(allRoutes)
    return allRoutes

def getBestRoute(source, desti):

    dest =  desti
    transit = cities
    transit.remove(source)
    transit.remove(dest)
    toTransit = []

    # Depth of search algo
    # for best result use searchDepth = minTransits
    # Exponentially increases search time
    searchDepth = minTransits

    # Width of search algo
    # defines how many cities should be considered as transit at each depth level
    searchWidth = 3 #len(cities)

    currTransits = 0
    current = source
    totalCost = 0
    while (currTransits < minTransits):

        toTransit.extend(bestRoute(current, transit, searchDepth, searchWidth, currTransits))

        currTransits = len(toTransit)
        for t in toTransit:
            try:
                transit.remove(t)
            except KeyError:
                pass

        current = toTransit[len(toTransit) - 1]

        totalCost += bestcost

    return toTransit


def partition(arr, low, high,compareVal = 2):


    i = (low - 1)
    pivot = arr[high][compareVal]

    for j in range(low, high):

        if arr[j][compareVal] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = deepcopy(arr[high]), deepcopy(arr[i + 1])
    return (i + 1)


def quickSort(arr, low, high, val = 2 ):

    if low < high:
        pi = partition(arr, low, high,compareVal=val)
        t1 = Thread( target=quickSort, args=(arr, low, pi - 1, val))
        t2 = Thread( target=quickSort, args=(arr, pi + 1, high,val))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    return arr

def getXClosest(cityDist, X):
    quickSort(cityDist, 0, len(cityDist) - 1)

    length = len(cityDist)

    if(X > length):
        X = length

    closest = []
    for count in range(X):

        closest.append(cityDist[count])

    return closest


def bestRoute(current, transit, maxDepth, maxWidth, currTransits, allRoutes = []):
    global bestcost

    bestcost = -1
    current_depth = 1

    # Calculate distance between current node and list of transitable cities
    # Stores it in cityDist
    # Format:
    # ityDist[index][0] = city name
    # cityDist[index][0] = distance of current node to source
    # cityDist[index][0] = distance of current node to source + current node to destination
    cityDist = []


    count = 0
    threads = []
    for city in transit:
        t = thread_fetchDist2(current, city, count, cityDist, dest)
        t.start()
        threads.append(t)
        count += 1

    for t in threads:
        t.join()

    # Get X number closest cities to destination
    closest = getXClosest(cityDist, maxWidth)

    best_route = []
    threads = []
    for x in closest:

        route = []
        route.append(x[0])


        t2 = thread_copyTransit(transit, x)
        t2.start()

        t3 = thread_copyCitydist(cityDist, x)
        t3.start()

        transit_copy = t2.join()
        cityDist_copy = t3.join()



        t = ThreadWithReturnValue(target=bestRoute2, args=(x[0], route, transit_copy, cityDist_copy, current_depth, maxDepth, maxWidth, 0,currTransits + 1, allRoutes))
        t.start()
        threads.append(t)


    for t in threads:
        Route = t.join()
        if (Route == []):
            continue

        # If generated route is better, assign it as best_route
        if (Route[len(Route) - 1] <= bestcost or bestcost == -1):
            best_route = deepcopy(Route)
            bestcost = best_route[len(best_route) - 1]
            best_route.remove(bestcost)

    return best_route

def bestRoute2(current, route, transit, cityDist, currDepth, maxDepth, maxWidth, currCost, currTransits , allRoutes = []):
    global bestcost

    currDepth += 1

    nextCost = lc.getDistance(route[len(route) - 1], dest)
    totalCost = nextCost + currCost

    if (currTransits >= minTransits):
        allRoutes.append(route)
        route.append(totalCost)
        return route
    elif (totalCost > bestcost and bestcost != -1):
        return []
    elif (currDepth > maxDepth):
        route.append(totalCost)
        return route

    # Calculate distance between current node and list of transitable cities
    # Stores it in cityDist
    # Format:
    # ityDist[index][0] = city name
    # cityDist[index][0] = distance of current node to source
    # cityDist[index][0] = distance of current node to source + current node to destination
    count = 0
    threads = []
    for city in cityDist:
        t= thread_fetchDist(current, city, count, cityDist)
        t.start()
        threads.append(t)
        count += 1

    for t in threads:
        t.join()

    closest = getXClosest(cityDist, maxWidth)

    best_route = []
    threads = []

    for x in closest:
        # Create copy before passing it to next level

        t1 = thread_copyRoute(route, x)
        t1.start()

        t2 = thread_copyTransit(transit, x)
        t2.start()

        t3 = thread_copyCitydist(cityDist, x)
        t3.start()

        route_copy = t1.join()
        transit_copy = t2.join()
        cityDist_copy = t3.join()

        # Cost/Distance from current node to X
        cost = x[2] - x[1]

        t = ThreadWithReturnValue(target=bestRoute2, args=(x[0], route_copy, transit_copy, cityDist_copy, currDepth, maxDepth, maxWidth, currCost + cost, currTransits + 1,allRoutes))
        t.start()
        threads.append(t)


    for t in threads:
        Route = t.join()

        if (Route == []):
            continue
        # If generated route is better, assign it as best_route
        if (Route[len(Route) - 1] <= bestcost or bestcost == -1):
            best_route = deepcopy(Route)
            bestcost = best_route[len(best_route) - 1]

    return best_route

class thread_fetchDist(threading.Thread):
    def __init__(self, current, city, cityID, cityDist):
        threading.Thread.__init__(self)
        self.current = current
        self.city = city
        self.cityID = cityID
        self.cityDist = cityDist

    def run(self):
        dist1 = lc.getDistance(self.current, self.city[0])
        dist2 = self.city[1]
        tDist = dist1 + dist2
        self.cityDist[self.cityID][2] = tDist

class thread_fetchDist2(threading.Thread):
    def __init__(self, current, city, cityID, cityDist, dest):
        threading.Thread.__init__(self)
        self.current = current
        self.city = city
        self.cityID = cityID
        self.cityDist = cityDist
        self.dest = dest

    def run(self):
        dist1 = lc.getDistance(self.current, self.city)
        dist2 = lc.getDistance(self.city, self.dest)

        tDist = dist1 + dist2
        self.cityDist.append([self.city, dist2, tDist])

#For easy multithreading with return values
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,**self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

class thread_copyRoute(threading.Thread):
    def __init__(self, route,x):
        threading.Thread.__init__(self)
        self.route = route
        self.route_copy = None
        self.x = x
    def run(self):
        self.route_copy = deepcopy(self.route)
        self.route_copy.append(self.x[0])
    def join(self):
        Thread.join(self)
        return self.route_copy

class thread_copyTransit(threading.Thread):
    def __init__(self, transit,x):
        threading.Thread.__init__(self)
        self.transit = transit
        self.transit_copy = None
        self.x = x
    def run(self):
        self.transit_copy = deepcopy(self.transit)
        self.transit_copy.remove(self.x[0])
    def join(self):
        Thread.join(self)
        return self.transit_copy

class thread_copyCitydist(threading.Thread):
    def __init__(self, cityDist,x):
        threading.Thread.__init__(self)
        self.cityDist = cityDist
        self.cityDist_copy = None
        self.x = x
    def run(self):
        self.cityDist_copy = deepcopy(self.cityDist)
        self.cityDist_copy.remove(self.x)
    def join(self):
        Thread.join(self)
        return self.cityDist_copy
