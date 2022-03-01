from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import json
import sys
import os
import uvicorn


from module import CountryReader
from module import Feature
from module import FeatureCollection

description = """
🚀
## Country Finder Api

"""

app = FastAPI(
    title="Spatial Country Game",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/terms/",
    contact={
        "name": "Spatial Country Game",
        "url": "http://killzonmbieswith.us/contact/",
        "email": "chacha@killzonmbieswith.us",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


#####################################################


# class Country(BaseModel):
#     name: Optional[str] = None
#     continent: Optional[str] = None


"""
  _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
 | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
 | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
 | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \
 | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
 |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/
"""
# FIX FOR YOUR ENVIRONMENT!
dataPath = "/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/country_and_city_data/country_by_continent"
europe = CountryReader(os.path.join(dataPath, "Europe.json"))


def centroid(vertexes):
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return (_x, _y)


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/
"""


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@app.get("/country_names/")
async def getCountryNames():
    """
    Description:
        Get country names
    Params:

    Returns:
        list / json
    """
    names = europe.getNames()
    return names


@app.get("/country/{country_name}")
async def getCountry(country_name):
    """
    Description:
        Get a country polygon given some country name
    Params:

    Returns:
        dict / json
    """
    polys = europe.getPolygons(country_name)
    return polys


@app.get("/countryCenter/{country_name}")
async def countryCenter(country_name):
    """
    Description:
        Get a country polygon given some country name
    Params:

    Returns:
        dict / json
    """
    coll = FeatureCollection()
    centers = []
    polys = europe.getPolygons(country_name)

    i = 0
    for poly in polys["geometry"]["coordinates"]:
        # print(poly[0])
        center = centroid(poly[0])
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": center},
            "properties": {"id": i},
        }
        centers.append(center)
        coll.addFeature(feature=feature)
        i += 1
    print(coll)
    return centers


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8006, log_level="info", reload=True)
