#!/usr/bin/python3

import overpy
import geopy
import urllib

# ===== HANDY PARAMETERS TO MESS WITH =====
bbox = "44.09635, -103.2024937, 44.1001, -103.1798"
searchPrefix = "https://duckduckgo.com/?q="
# ===== END HANDY PARAMETERS =====

overpass = overpy.Overpass(url = "https://lz4.overpass-api.de/api/interpreter")
nominatim = geopy.geocoders.Nominatim(user_agent = "missing-tag-helper")

def getSearchLink(name: str, city: str, state: str):
    search = name + " " + city + " " + state
    return searchPrefix + urllib.parse.quote(search)

result = overpass.query("""
    nw ( """ + bbox + """)
    [amenity~"^(cafe|restaurant|fast_food)$"]
    [!opening_hours];
    out tags center;
    """)

# just get the city and state once so we don't make Nominiatim mad,
#  it's probably safe to assume they're all in the same city
address = None
city = None
state = None
firstRun = True

for category in (result.ways, result.nodes, result.relations):
    for element in category:
        if firstRun:
            firstRun = False
            if type(element) is overpy.Way:
                lat = element.center_lat
                lon = element.center_lon
            elif type(element) is overpy.Node:
                lat = element.lat
                lon = element.lon
            query = str(lat) + "," + str(lon)
            address = nominatim.reverse(query)
            city = address.raw['address']['city']
            state = address.raw['address']['state']

        if 'name' in element.tags:
            print(getSearchLink(element.tags['name'], city, state))
        else:
            print("Empty name for", type(element), "with id", element.id)
