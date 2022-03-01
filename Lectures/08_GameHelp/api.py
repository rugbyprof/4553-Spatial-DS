from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import json
import sys
import uvicorn

from module import Feature
from module import FeatureCollection
from module import CountryReader

description = """
🚀
The Bacon number of an actor is the number of degrees of separation he or she has from Bacon, as defined by the game. This is an application of the Erd
ős number concept to the Hollywood movie industry. The higher the Bacon number, the greater the separation from Kevin Bacon the actor is.

The computation of a Bacon number for actor X is a "shortest path" algorithm, applied to the co-stardom network:

* Kevin Bacon himself has a Bacon number of 0.
* Those actors who have worked directly with Kevin Bacon have a Bacon number of 1.
* If the lowest Bacon number of any actor with whom X has appeared in any movie is N, X's Bacon number is N+1.

## Examples
#### Elvis Presley:

* Elvis Presley was in Change of Habit (1969) with Edward Asner
* Edward Asner was in JFK (1991) with Kevin Bacon

Therefore, Asner has a Bacon number of 1, and Presley (who never appeared in a film with Bacon) has a Bacon number of 2.

#### Ian McKellen:

* Ian McKellen was in X-Men: Days of Future Past (2014) with Michael Fassbender and James McAvoy
* McAvoy and Fassbender were in X-Men: First Class (2011) with Kevin Bacon

Therefore, McAvoy and Fassbender have Bacon numbers of 1, and McKellen has a Bacon number of 2.
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


class Movie(BaseModel):
    startYear: Optional[int] = None
    movieId: Optional[str] = None
    movieTitle: Optional[str] = None


"""
  _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
 | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
 | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
 | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \
 | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
 |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/
"""

None


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


@app.get("/country/")
async def getCountry():
    """
    Description:
        Get all docs dealing with Kevin Bacon movie titles
    Params:

    Returns:
        dict / json
    """
    return None


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8006, log_level="info", reload=True)
