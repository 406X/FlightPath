import Location as lc
from copy import deepcopy

#Version 1
#Contains:
# -Basic A* search (Fastest result)
# -Heuristic depth first search (Slower but better result)

cities = []
minTransits = 0
dest = ""
bestcost = -1

#Basic A* Search Algo
def getRoute(source, dest):
    transit = cities
    transit.remove(source)
    transit.remove(dest)
    transitCount = 0
    toTransit = []
    totalDist = 0

    current = source

    while (True):
        shortestVal = -1;
        shortestNext = ""
        shortestD2 = 0

        for city in transit:
            dist1 = lc.getDistance(current, city)
            dist2 = lc.getDistance(city, dest)
            tDist = dist1 + dist2

            if (shortestVal == -1):
                shortestVal = tDist
                shortestNext = city
                shortestD2 = dist2
            elif (shortestVal > tDist):
                shortestVal = tDist
                shortestNext = city
                shortestD2 = dist2

        toTransit.append(shortestNext)

        transit.remove(shortestNext)

        cost = shortestVal - shortestD2
        totalDist += cost
        current = shortestNext

        transitCount += 1
        if (transitCount >= minTransits):
            totalDist += shortestD2
            # print(toTransit)
            # print(totalDist)
            return toTransit


#Heuristic depth first search
def getRoute_v2(source, dest):
    transit = cities
    transit.remove(source)
    transit.remove(dest)
    toTransit = []

    # Depth of search algo
    # for best result it should be as close as possible to min transit
    # Exponentially increases search time
    searchDepth = 5

    # Width of search algo
    # defines how many cities should be considered as transit at each depth
    # low effect on search results
    searchWidth = 3

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


def partition(arr, low, high):
    compareVal = 2
    i = (low - 1)
    pivot = arr[high][compareVal]

    for j in range(low, high):

        if arr[j][compareVal] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = deepcopy(arr[high]), deepcopy(arr[i + 1])
    return (i + 1)


def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)

        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def getXClosest(cityDist, X):
    quickSort(cityDist, 0, len(cityDist) - 1)

    closest = []
    for count in range(X):
        closest.append(cityDist[count])

    return closest


def bestRoute(current, transit, maxDepth, maxWidth, currTransits):
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
    for city in transit:
        dist1 = lc.getDistance(current, city)
        dist2 = lc.getDistance(city, dest)

        tDist = dist1 + dist2
        cityDist.append([city, dist2, tDist])

    # Get X number closest cities to destination
    closest = getXClosest(cityDist, maxWidth)

    best_route = []

    for x in closest:

        route = []
        route.append(x[0])

        # Create copy before passing it to next level
        transit_copy = deepcopy(transit)
        transit_copy.remove(x[0])
        cityDist_copy = deepcopy(cityDist)
        cityDist_copy.remove(x)

        # Cost/Distance from current node to X
        cost = x[2] - x[1]

        # recursive call to calculate next city to transit
        Route = bestRoute2(x[0], route, transit_copy, cityDist_copy, current_depth, maxDepth, maxWidth, cost,
                           currTransits + 1)

        if (Route == []):
            continue

        # If generated route is better, assign it as best_route
        if (Route[len(Route) - 1] <= bestcost or bestcost == -1):
            best_route = deepcopy(Route)
            bestcost = best_route[len(best_route) - 1]

            best_route.remove(bestcost)

    return best_route


def bestRoute2(current, route, transit, cityDist, currDepth, maxDepth, maxWidth, currCost, currTransits):
    global bestcost

    currDepth += 1

    nextCost = lc.getDistance(route[len(route) - 1], dest)
    totalCost = nextCost + currCost

    if (currTransits >= minTransits):
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
    for city in cityDist:
        dist1 = lc.getDistance(current, city[0])
        dist2 = city[1]

        tDist = dist1 + dist2
        cityDist[count][2] = tDist
        count += 1

    # Get X number closest cities to destination
    closest = getXClosest(cityDist, maxWidth)

    best_route = []

    # Calculate next route for each city in <closest>
    for x in closest:

        # Create copy before passing it to next level
        route_copy = deepcopy(route)
        route_copy.append(x[0])
        transit_copy = deepcopy(transit)
        transit_copy.remove(x[0])
        cityDist_copy = deepcopy(cityDist)
        cityDist_copy.remove(x)

        # Cost/Distance from current node to X
        cost = x[2] - x[1]

        # recursive call to calculate next city to transit
        Route = bestRoute2(x[0], route_copy, transit_copy, cityDist_copy, currDepth, maxDepth, maxWidth,
                           currCost + cost, currTransits + 1)

        if (Route == []):
            continue

        # If generated route is better, assign it as best_route
        if (Route[len(Route) - 1] <= bestcost or bestcost == -1):
            best_route = deepcopy(Route)
            bestcost = best_route[len(best_route) - 1]

    return best_route