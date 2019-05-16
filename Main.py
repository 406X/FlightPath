import Location as lc
import webbrowser
import os
import RouteV3 as RT
from mako.template import Template
import time


#Variables
minTransits = 3
source = "Kuala Lumpur"
dest= "Johor Bahru"
cities = { "Alor Setar", "Malacca", "Kota Bahru", "Seremban", "Kuantan", "Ipoh", "Kangar", "Shah Alam", "Kuala Terrengganu", "Johor Bahru","Kota Kinabalu","Kuching","Kuala Lumpur"}

API_KEY = "AIzaSyAn27el7Uuj1qLQvpZgF9fbVjGLu_HPhbQ"
# Google Cloud API Key
# This program uses the following Google Cloud APIs
# - Distance Matrix
# - Geocoding API
# - Maps JavaScript API

#Init
RT.cities = cities
RT.dest = dest
RT.minTransits = minTransits
lc.API_KEY = API_KEY

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
    global source
    global minTransits
    list = cities.copy()
    print("Enter a starting location:")
    print("Available options:")
    for c in list:
        print(" -" + c)
    source = input("Input: ")
    list.remove(source)

    print("Enter destination location:")
    print("Available options:")
    for c in list:
        print(" -" + c)
    dest = input("Input: ")
    list.remove(dest)
    num = input("Number of transits to make (1-5) : ")
    RT.minTransits = int(num)


print("Generating route...")

#start()

startTime = time.time()
route = RT.getRoute_v2(source,dest)
print("Transits: " +str(route))

end = time.time()
print("Time:")
print(end - startTime)

showRoute(route)

