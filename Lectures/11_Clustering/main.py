from numpy import where
from sklearn.datasets import make_classification
from matplotlib import pyplot
import utm
import json
from rich import print



bandOffset = {
    "X": 10,
    "W": 9,
    "V": 8,
    "U": 7,
    "T": 6,
    "S": 5,
    "R": 4,
    "Q": 3,
    "P": 2,
    "N": 1,
    "M": 1,
    "L": 2,
    "K": 3,
    "J": 4,
    "H": 5,
    "G": 6,
    "F": 7,
    "E": 8,
    "D": 9,
    "C": 10,
}


def affinity():
    # affinity propagation clustering
    from numpy import unique
    from numpy import where
    from sklearn.datasets import make_classification
    from sklearn.cluster import AffinityPropagation
    from matplotlib import pyplot

    # define dataset
    X, _ = make_classification(
        n_samples=1000,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_clusters_per_class=1,
        random_state=4,
    )
    print(X)
    # define the model
    model = AffinityPropagation(damping=0.9)
    # fit the model
    model.fit(X)
    # assign a cluster to each example
    yhat = model.predict(X)
    # retrieve unique clusters
    clusters = unique(yhat)
    # create scatter plot for samples from each cluster
    for cluster in clusters:
        # get row indexes for samples with this cluster
        row_ix = where(yhat == cluster)
        # create scatter of these samples
        pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # show the plot
    pyplot.show()


def sillyProjection(xMax, yMax, utmCoord):
    pass


def ll2xy(lon, lat=None):
    if isinstance(lon, list):
        lon, lat = lon

    lon = float(lon)
    lat = float(lat)

    xy = utm.from_latlon(lat, lon)

    return xy


def utm2xy(easting, northing, zone, band):
    pass


def loadUfos():
    with open("ufo_data.geojson") as f:
        ufos = json.load(f)

    return ufos


def countUnique():
    uniqueBands = {}
    uniqueZones = {}
    ufos = loadUfos()

    for ufo in ufos["features"]:
        easting, northing, zone, band = ll2xy(ufo["geometry"]["coordinates"])
        if not band in uniqueBands:
            uniqueBands[band] = 0
        uniqueBands[band] += 1

        if not zone in uniqueZones:
            uniqueZones[zone] = 0
        uniqueZones[zone] += 1

    print(uniqueBands)
    print(uniqueZones)


if __name__ == "__main__":
    # affinity()

    ufos = loadUfos()

    # ( 6,400,000 x 2π ) x ( 80° / 360° ) = 8,936,085 (for Northing)
    # ( 6,400,000 x 2π ) x ( 3° / 360° ) = 335,103 (for Easting)

# - UTM zones are all 6 degrees wide and increase from west to east starting at the -180 degree mark.
# - Calculate the eastern boundary of any UTM zone by multiplying the zone number by 6 and substract 180.
# - Subtract 6 degrees to obtain the western boundary.
# - Therefore to find the eastern boundary of UTM zone 11: 
#    - Eastern boundary of zone 11 = (11 * 6) – 180 = -114 degrees.
#    - Western boundary of zone 11 = -114 – 6 = -120 degrees.

    maxEasting = 335103 * 2
    maxEasting = 500000 * 2

    for ufo in ufos["features"]:
        easting, northing, zone, band = ll2xy(ufo["geometry"]["coordinates"])

        # if easting > 500000:
        #     easting -= 500000

        #     ratio = easting / maxEasting
        # else:
        #     easting = 500000 - easting
        #     ratio = easting / maxEasting

        ratio = easting / maxEasting

        print(easting, northing)

    # print((500000 - 335103) / maxEasting)
    # print((500000 + 335103) / maxEasting)
