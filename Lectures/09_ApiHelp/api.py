# Libraries for FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Builtin libraries
from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
import os

from random import shuffle

# Classes from my module
from module import CountryReader
from module import Feature
from module import FeatureCollection

"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""

description = """🚀
## Worldle Clone
### With Better Distance Calculations
"""

# Needed for CORS
origins = ["*"]


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="Worldle Clone",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/worldleterms/",
    contact={
        "name": "Worldle Clone",
        "url": "http://killzonmbieswith.us/worldle/contact/",
        "email": "chacha@killzonmbieswith.us",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Needed for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
  _      ____   _____          _         _____ _                _____ _____ ______  _____
 | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
 | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
 | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \
 | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
 |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/

This is where you will add code to load all the countries and not just countries. Below is a single
instance of the class `CountryReader` that loads countries. There are 6 other continents to load or
maybe you create your own country file, which would be great. But try to implement a class that 
organizes your ability to access a countries polygon data.
"""

# FIX FOR YOUR OWN ENVIRONMENT! This is my path
BIG_file = "countries_stanford.geojson"
small_file = "countries.geojson"

dataPath = "/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/country_and_city_data/"
countryDB = CountryReader(os.path.join(dataPath, BIG_file))


"""
  _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
 | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
 | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
 | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \
 | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
 |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/

I place local methods either here, or in the module we created. I'm leaving it here to help
with the lecture we had in class, but it can easily be moved then imported. In fact you should
move it if you have other "spatial" methods that it can be packaged with in the module folder. 
"""


def centroid(polygon):
    """Calculates the centroid point for a polygon (linear ring of points)
    Params:
        polygon (list)  : List of lon/lat points representing a polygon
    Returns:
        tuple : (x,y) or lon,lat coords representing the center point
    """
    xList = [vertex[0] for vertex in polygon]
    yList = [vertex[1] for vertex in polygon]
    polyLen = len(polygon)
    x = sum(xList) / polyLen
    y = sum(yList) / polyLen
    return (x, y)


def compass_bearing(pointA, pointB):
    """Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2(sin(Δlong).cos(lat2),cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    Source:
        https://gist.github.com/jeromer/2005586
    Params:
        pointA  : The tuple representing the latitude/longitude for the first point. Latitude and longitude must be in decimal degrees
        pointB  : The tuple representing the latitude/longitude for the second point. Latitude and longitude must be in decimal degrees
    Returns:
        (float) : The bearing in degrees
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def countryCentroid(name):
    """Get the centroid of a country by finding the largest polygon and
        calculating the centroid on that polygon only
    Params:
        name (string): name of country
    Returns:
        (tuple): point (x,y)
    """
    countryPolys = countryDB.getPolygons(name)
    print(countryPolys)

    largest = largestPoly(countryPolys["geometry"]["coordinates"])
    center = centroid(largest)
    return center


def countryPoly(country):
    """Grab the country polygon from the country "DB" (really a country reader class I wrote for you guys).
    Params:
        country (string)   : name of the country you want the polygon for
    Returns:
        polygon (feature/dict) : feature pulled from the countries feature collection.
    """
    # lowercase the country name then capitalize to fit the existing names.
    country = country.lower().title()

    # Go get the polygons
    polys = countryDB.getPolygons(country)

    largest = largestPoly(polys["geometry"]["coordinates"])

    if not polys:
        return {"Error": f"Country: {country} didn't exist!"}

    return largest


def DistancePointLine(px, py, x1, y1, x2, y2):
    """Calculates the distance from a given point (px,py), to the line segment (x1,y1) , (x2,y2).
    Params:
        px (float) : decimal degrees longitude of point
        py (float) : decimal degrees latitude of point
        x1 (float) : decimal degrees longitude of line start
        y1 (float) : decimal degrees latitude of line start
        x1 (float) : decimal degrees longitude of line end
        y1 (float) : decimal degrees latitude of line end
    Returns:
        distanc (float) : distance from point to line segment

    """
    # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
    LineMag = lineMagnitude(x1, y1, x2, y2)

    if LineMag < 0.00000001:
        DistancePointLine = 9999
        return DistancePointLine

    u1 = ((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1))
    u = u1 / (LineMag * LineMag)

    if (u < 0.00001) or (u > 1):
        # // closest point does not fall within the line segment, take the shorter distance
        # // to an endpoint
        ix = lineMagnitude(px, py, x1, y1)
        iy = lineMagnitude(px, py, x2, y2)
        if ix > iy:
            DistancePointLine = iy
        else:
            DistancePointLine = ix
    else:
        # Intersecting point is on the line, use the formula
        ix = x1 + u * (x2 - x1)
        iy = y1 + u * (y2 - y1)
        DistancePointLine = lineMagnitude(px, py, ix, iy)

    return DistancePointLine


def haversineDistance(lon1, lat1, lon2, lat2, units="miles"):
    """Calculate the great circle distance in kilometers between two points on the earth (start and end) where each point
        is specified in decimal degrees.
    Params:
        lon1  (float)  : decimel degrees longitude of start (x value)
        lat1  (float)  : decimel degrees latitude of start (y value)
        lon2  (float)  : decimel degrees longitude of end (x value)
        lat3  (float)  : decimel degrees latitude of end (y value)
        units (string) : miles or km depending on what you want the answer to be in
    Returns:
        distance (float) : distance in whichever units chosen
    """
    radius = {"km": 6371, "miles": 3956}

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = radius[units]  # choose miles or km for results
    return c * r


def largestPoly(polygons):
    """Simple implementation to grab the "hopefully" biggest polygon for a country
        (aside from island nations / arcapelligos) that represents the "actual" country.
    Params:
        polygons (list) : list of polygons
    Returns:
        list : the biggest polygon in the list
    """
    i = 0
    max = 0
    index = 0
    for poly in polygons:
        print(len(poly[0]))
        print(poly[0])
        print("")
        if len(poly[0]) > max:
            max = len(poly[0])
            print(max)
            index = i
        i += 1
    return polygons[index][0]


def lineMagnitude(x1, y1, x2, y2):
    """Calculate the magnitude of a line. This is a type of distance function. Not the same as `haversine` but is used
        in conjunction the the `DistancePointLine` method below.
        Source: https://maprantala.com/2010/05/16/measuring-distance-from-a-point-to-a-line-segment-in-python/
    Params:
        x1 (float) : decimal degrees longitude of line start
        y1 (float) : decimal degrees latitude of line start
        x1 (float) : decimal degrees longitude of line end
        y1 (float) : decimal degrees latitude of line end
    Returns:
        Magnitude (float) of the line (aka distance).
    """
    lineMagnitude = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
    return lineMagnitude


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/

 This is where your routes will be defined. Remember they are really just python functions
 that will talk to whatever class you write above. Fast Api simply takes your python results
 and packagres them so they can be sent back to your programs request.
"""


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/country_names/")
async def getCountryNames():
    """
    ### Description:
        Get country names. This example is limited to Africa, but your version
        should include all the countries of the world.
    ### Params:
        None
    ### Returns:
        list : json encoded list of country names
    ## Examples:
    [http://127.0.0.1:8080/country_names/](http://127.0.0.1:8080/country_names/)
    ### Results:
    ```json
    [
        "Afghanistan",
        "Angola",
        "Albania",
        "United Arab Emirates",
        "Argentina",
        "Armenia",
        "Antarctica",
        "Fr. S. Antarctic Lands",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Burundi",
        "Belgium",
        "Benin",
        "Burkina Faso",
        "Bangladesh",
        "Bulgaria",
        "Bahamas",
        "Bosnia and Herz.",
        "Belarus",
        ...
    ]
    """
    names = countryDB.getNames()
    if names:
        return names
    else:
        return {"Error": "Names list was empty or None."}


@app.get("/country/{country_name}")
async def getCountry(country_name, coords_only: bool = False):
    """
    ### Description:
        Get a country polygon given a country name.
    ### Params:
        country_name (str)  : A country name to search for
    ### Returns:
        dict / json
    ## Example:
    [http://127.0.0.1:8080/country/chad](http://127.0.0.1:8080/country/chad)
    ### Results:
    ```json
    {
        "type": "Feature",
        "id": "kk522dt9425.221",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
            [
                [
                [
                    23.98130579,
                    19.49612376
                ],
                [
                    23.98151249,
                    19.2638382
                ],
        ...
    }
    ```
    [http://127.0.0.1:8080/country/Niger?coords_only=True](http://127.0.0.1:8080/country/Niger?coords_only=True)

    ```json
    ### Results:
    [
      [
        [
        [
            23.98130579,
            19.49612376
        ],
        [
            23.98151249,
            19.2638382
        ],
        [
            23.9817192,
            19.03155263
        ],
        ...
    ]
    ```
    """
    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    # Go get the polygons
    polys = countryDB.getPolygons(country_name)

    largest = largestPoly(polys["geometry"]["coordinates"])

    if not polys:
        return {"Error": f"Country: {country_name} didn't exist!"}

    # Remove extra geodata info if coords_only is True
    if coords_only:
        return largest

    f = Feature(coords=largest, properties={"name": country_name})

    fc = FeatureCollection()
    fc.addFeature(feature=f)

    return fc


@app.get("/countryCenter/{country_name}")
async def countryCenter(country_name, raw: bool = False):
    """
    ### Description:
        Get a point that represents the spatial center of a countries polygon.
    ### Params:
        country_name (str)  : A country name to search for
    ### OptionalParams
        raw (bool)          : True = send coords only, no feature crap
    ### Returns:
        dict : json Feature collection
        list : center point (if raw = True)
    ## Examples:

    [http://127.0.0.1:8080/countryCenter/united%20kingdom](http://127.0.0.1:8080/countryCenter/united%20kingdom)

    ### Results:
    ```json
    {
        "type": "FeatureCollection",
        "features": [
            {
            "feature": {
                "type": "Feature",
                "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.082751279583333,
                    54.005709779374996
                ]
                },
                "properties": {
                "name": "United Kingdom"
                }
            }
            }
        ]
    }
    ```

    [http://127.0.0.1:8080/countryCenter/united%20kingdom?raw=true](http://127.0.0.1:8080/countryCenter/united%20kingdom?raw=true)

    ### Results:
    ```json
    [
        -3.082751279583333,
        54.005709779374996
    ]
    ```
    """
    # print("hello yall")
    # print(country_name)
    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    coll = FeatureCollection()
    centers = []
    country = countryDB.getPolygons(country_name)
    largest = largestPoly(country["geometry"]["coordinates"])

    print(largest)
    center = centroid(largest)

    if raw:
        return center

    feature = Feature(
        coords=center, type="Point", properties={"name": country["properties"]["name"]}
    )
    centers.append(center)
    coll.addFeature(feature=feature)

    return coll.to_json()


@app.get("/country_lookup/{key}")
async def getCountryPartialMatch(key):
    """
    ### Description:
        Get country names that partially match the key passed in.
    ### Params:
        key (str)  : a substring compared with the beginning of every country name.
    ### Returns:
        list / json

    ## Example:
    [http://127.0.0.1:8080/country_lookup/ga](http://127.0.0.1:8080/country_lookup/ga)

    ### Results:
    ```json

    [
    "Gabon",
    "Gambia"
    ]
    """
    key = key.lower()
    partial = []
    names = countryDB.getNames()
    for name in names:
        low_name = name.lower()
        if low_name.startswith(key):
            partial.append(name)
    return partial


@app.get("/line_between/")
async def getLineBetween(start: str = None, end: str = None):
    """
    ### Description:
        Get a line feature that connects two country centroids
    ### Params:
        start (str) : country name
        end (str) : country name
    ### Returns:
        feature / coords
    ## Example:

    [http://localhost:8080/line_between/?start=finland&end=greenland](http://localhost:8080/line_between/?start=finland&end=greenland)

    ### Results:
    ```json
    {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
            [
                [
                25.83077124897437,
                65.34954882461537
                ],
                [
                -40.8824912878788,
                74.1543870603788
                ]
            ]
            ]
        },
        "properties": {
            "from": "finland",
            "to": "greenland"
        }
    }
    ```
    """
    p1 = countryCentroid(start)
    p2 = countryCentroid(end)

    feature = Feature(
        coords=[[p1, p2]],
        type="LineString",
        properties={"from": start, "to": end},
    )

    return feature.to_json()


@app.get("/property/{country}")
async def getProperty(country, key: str = None, allKeys: bool = False):
    """
    ### Description:
        Get a property from a country or all of them.
    ### Params:
        country (str)  : name of the country
        key (str) : the key value in the properties dictionary
        allKeys (bool) : return all the property keys
    ### Returns:
        bearingious : string, object, list, etc.
    ## Examples:

    [http://127.0.0.1:8080/property/france?key=bbox](http://127.0.0.1:8080/property/france?key=bbox)

    #### Response:
    ```
    [
        -54.5247542,
        2.05338919,
        9.56001631,
        51.14850617
    ]
    ```

    [http://127.0.0.1:8080/property/united%20kingdom?allKeys=false](http://127.0.0.1:8080/property/united%20kingdom?allKeys=false)

    #### Response:
    ```
    {
        "scalerank": 1,
        "featurecla": "Admin-0 country",
        "labelrank": 2,
        "sovereignt": "United Kingdom",
        "sov_a3": "GB1",
        "adm0_dif": 1,
        "level": 2,
        "type": "Country",
        "admin": "United Kingdom",
        "adm0_a3": "GBR",
        "geou_dif": 0,
        "geounit": "United Kingdom",
        "gu_a3": "GBR",
        "su_dif": 0,
        "subunit": "United Kingdom",
        "su_a3": "GBR",
        ...
    }
    ```
    """

    # lowercase the country name then capitalize to fit the existing names.
    country = country.lower().title()
    data = countryDB.getProperties(country)

    if key:
        return data[key]

    if allKeys:
        return list(data.keys())

    return data


@app.get("/randomCountry/")
async def getRandomCountry():
    """ """
    names = countryDB.getNames()
    shuffle(names)
    target = names[0]
    poly = countryPoly(target)
    print(target)

    country = countryDB.getPolygons(target)
    largest = largestPoly(country["geometry"]["coordinates"])

    print(largest)
    center = centroid(largest)

    return {"name": target, "poly": poly, "center": center}


@app.get("/bbox/{country}")
async def getBbox(country, raw: bool = False):
    """
    ### Description:
        Get a polygon formattexd bbox from a country's properties.
    ### Params:
        country (str)  : name of the country
        raw (bool) : return the raw bounding box (extremes W,S,E,N) and not a polygon
    ### Returns:
        list/Feature : either raw list of extreme points, or a feature with a polygon bbox
    ## Examples:
    [http://127.0.0.1:8080/bbox/united%20kingdom?raw=false](http://127.0.0.1:8080/bbox/united%20kingdom?raw=false)
    #### Response:
    ```
        {
        "feature": {
                "type": "Feature",
                "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                                [
                                        [
                                                -7.57216793,
                                                49.9599999
                                        ],
                                        [
                                                1.6815308,
                                                49.9599999
                                        ],
                                        [
                                                1.6815308,
                                                58.63500011
                                        ],
                                        [
                                                -7.57216793,
                                                58.63500011
                                        ],
                                        [
                                                -7.57216793,
                                                49.9599999
                                        ]
                                ]
                        ]
                },
                "properties": {
                        "country": "United Kingdom"
                }
        }
    }
    ```
    [http://127.0.0.1:8080/bbox/ireland?raw=true](http://127.0.0.1:8080/bbox/ireland?raw=true)

    ### Response:
    ```
    [
        -9.97708574,
        51.66930126,
        -6.0329854,
        55.13162222
    ]
    ```
    """
    country = country.lower().title()
    bbox = countryDB.getBbox(country)

    if raw:
        return bbox

    west, south, east, north = tuple(bbox)

    poly = [[west, south], [east, south], [east, north], [west, north], [west, south]]

    feature = Feature(coords=[poly], properties={"country": country}).to_json()
    print(feature)
    return feature


@app.get("/bboxCenter/{country}")
async def getbboxCenter(country, raw: bool = False):
    """
    ### Description:
        Get a center point from a country's bbox.
    ### Params:
        country (str)  : name of the country
        raw (bool) : return the raw point and not a feature
    ### Returns:
        point/Feature : either center point [x,y], or a feature with the point in it
    ## Examples:
    [http://127.0.0.1:8080/centerPoint/united%20kingdom?raw=false](http://127.0.0.1:8080/centerPoint/united%20kingdom?raw=false)
    #### Response:
    ```
    {
    "feature":{
        "type":"Feature",
        "geometry":{
            "type":"Point",
            "coordinates":[
                -8.00503557,
                53.40046174
            ]
        },
        "properties":{
            "country":"Ireland"
        }
    }
    }
    ```
    [http://127.0.0.1:8080/centerPoint/ireland?raw=true](http://127.0.0.1:8080/centerPoint/ireland?raw=true)

    ### Response:
    ```
    [
        -8.00503557,
        53.40046174
    ]
    ```
    """
    country = country.lower().title()
    bbox = countryDB.getBbox(country)

    west, south, east, north = tuple(bbox)

    center = [(west + east) / 2.0, (north + south) / 2.0]

    if raw:
        return center

    feature = Feature(coords=center, properties={"country": country}).to_json()
    print(feature)
    return feature


@app.get("/centroidRelations/")
async def centroidRelations(start: str, end: str):
    """
    ### Description:
        Get the distance between 2 polygon centroids. This is meant for you to improve on!
        Also get the bearing between the two centroids.
    ### Params:
        start (str)  : name of country
        end (str) : name of country
    ### Returns:
        dict: {"distance":float, "bearing":float}
            distance in miles
            bearing between the two
        Line: A line feature between the two

    ## Examples:

    [http://localhost:8080/centroidRelations/?start=france&end=greece](http://localhost:8080/centroidRelations/?start=france&end=greece)

    ### Results
    ```json
    {
    "distance": 1114.8495334378304,
    "bearing": 109.29581652664211,
    "line": {
        "feature": {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
            [
                3.245872756458333,
                47.023721337291676
            ],
            [
                23.223037302790694,
                39.80152575325582
            ]
            ]
        },
        "properties": {
            "from": "france",
            "to": "greece"
        }
        }
    }
    }
    ```
    """
    lon1, lat1 = countryCentroid(start)
    lon2, lat2 = countryCentroid(end)

    feature = Feature(
        coords=[[lon1, lat1], [lon2, lat2]],
        type="LineString",
        properties={"from": start, "to": end},
    )

    print(lon1, lat1)
    print(lon2, lat2)

    # lon1, lat1, lon2, lat2,
    distance = haversineDistance(lon1, lat1, lon2, lat2)
    bearing = compass_bearing((lat1, lon1), (lat2, lon2))

    feature = feature.to_json()

    return {
        "distance": distance,
        "bearing": bearing,
        "line": feature,
    }


@app.get("/borderRelations/")
async def borderRelations(start: str, end: str):
    """
    ### Description:
        Get the distance between 2 polygons in a brute force fashion. This is meant for you to improve on!
    ### Params:
        start (str)  : name of country
        end (str) : name of country
    ### Returns:
        dict: {"closest":dict, "touching":list}
            closest =  the closest two points (if distance > 0)
            OR
            list of the points that are touching

    ## Examples:

    [http://127.0.0.1:8080/borderRelations/?start=germany&end=austria](http://127.0.0.1:8080/borderRelations/?start=germany&end=austria)

    ### Response:

    ```json
    {
    "closest": {
        "points": [],
        "distance": 0
    },
    "touching": [
        [
        13.59594567,
        48.87717194
        ],
        [
        13.24335737,
        48.41611481
        ],

        12.14135746,
        47.7030834
        ],
        [
        11.42641402,
        47.52376618
        ],
        ...
    ]
    }
    ```
    """
    poly1 = countryPoly(start)
    poly2 = countryPoly(end)

    min = 999999
    closest = {}
    touching = []

    for p1 in poly1:
        lon1, lat1 = p1
        for p2 in poly2:
            lon2, lat2 = p2
            d = haversineDistance(lon1, lat1, lon2, lat2)
            if d == 0:
                touching.append(p2)
            if d < min:
                min = d
                closest = {"points": [p1, p2], "distance": d}

    if len(touching) > 0:
        closest = {"points": [], "distance": 0}
    return {"closest": closest, "touching": touching}


@app.get("/lengthLine/{country}")
async def lengthLine(country):
    """
    ### Description:
        Get a line between the furthest two points within one country polygon.
    ### Params:
        country (str)  : name of country
    ### Returns:
        feature: line between furthest two points in a countries polygon

    ## Examples:

    [http://localhost:8080/lengthLine/germany](http://localhost:8080/lengthLine/germany)

    ### Response:

    ```json
    {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [
        [
            12.93262699,
            47.46764558
        ],
        [
            8.52622928,
            54.96274364
        ]
        ]
    },
    "properties": {
        "country": "germany",
        "distance": 551.2008987920657
    }
    }

    ```
    """
    poly = countryPoly(country)

    max = -999999

    for p1 in poly:
        lon1, lat1 = p1
        for p2 in poly:
            lon2, lat2 = p2
            d = haversineDistance(lon1, lat1, lon2, lat2)
            if d == 0:
                continue
            if d > max:
                max = d
                maxp1 = p1
                maxp2 = p2
                maxd = d

    feature = Feature(
        coords=[maxp1, maxp2],
        type="LineString",
        properties={"country": country, "distance": maxd},
    )

    return feature.to_json()


@app.get("/cardinal/{degrees}")
async def cardinal(degrees):
    """
    This method works returns the cardinal direction given a bearing in decimal degrees.
    Params:
        degrees (float) : decimal degrees
    Returns:
        cardinal direction (string) : N, NNE ..... NW, NNW

    ## Examples:

    [http://localhost:8080/cardinal/76](http://localhost:8080/cardinal/76)

    ### Response:

        ```json
        {
            "direction": "ENE",
            "image": "ENE.png",
            "img_tag": "<img src='./images/ENE.png'>"
        }
        ```
    """
    dirs = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    degrees = int(float(degrees))
    ix = int((degrees + 11.25) / 22.5)
    d = dirs[ix % 16]

    return {
        "direction": d,
        "image": str(d) + ".png",
        "img_tag": f"<img src='./images/{d}.png'>",
    }


@app.get("/pt2poly/")
async def pt2poly(x: float, y: float, scale: int = 1):
    scale = sum([0.05] * scale)
    poly = []
    poly.append([x, y])
    poly.append([x - scale, y])
    poly.append([x - scale, y - scale])
    poly.append([x, y - scale])
    poly.append([x, y])
    return poly


"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
