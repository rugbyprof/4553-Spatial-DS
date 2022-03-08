from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware

# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from typing import Optional
import uvicorn
from math import sqrt
from math import pow

# local built in's from python
import json
import sys
import os


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


def largestPoly(polygons):
    """Simple implementation to grab the "hopefully" biggest polygon
        for a country (aside from island nations / arcapelligos) that
        represents the "actual" country.
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


def getCountryCentroid(name):
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


# https://maprantala.com/2010/05/16/measuring-distance-from-a-point-to-a-line-segment-in-python/
def lineMagnitude(x1, y1, x2, y2):
    lineMagnitude = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
    return lineMagnitude


# Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def DistancePointLine(px, py, x1, y1, x2, y2):
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


# https://www.sitepoint.com/community/t/distance-between-long-lat-point-and-line-segment/50583/3

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
async def countryCenter(country_name):
    """
    ### Description:
        Get a point that represents the spaital center of a countries polygon.
    ### Params:
        country_name (str)  : A country name to search for
    ### OptionalParams
        feature_collection (bool) : default = False
    ### Returns:
        dict : json Feature collection
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
    """

    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    coll = FeatureCollection()
    centers = []
    country = countryDB.getPolygons(country_name)
    largest = largestPoly(country["geometry"]["coordinates"])

    print(largest)
    center = centroid(largest)

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
async def getLineBetween(countryA: str = None, countryB: str = None):
    """
    ### Description:
        Get country names that partially match the key passed in.
    ### Params:
        key (str)  : a substring compared with the beginning of every country name.
    ### Returns:
        list / json
    ### Example:

    """
    pointA = getCountryCentroid(countryA)
    pointB = getCountryCentroid(countryB)

    feature = Feature(
        coords=[[pointA, pointB]],
        type="LineString",
        properties={"from": countryA, "to": countryB},
    )

    return feature


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
        various : string, object, list, etc.
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

    feature = Feature(coords=[poly], properties={"country": country})
    print(feature)
    return feature


"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the variable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
