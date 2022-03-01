import os
import sys
import json

print(os.getcwd())


class CountryReader:
    def __init__(self, file_name, bbox=None):
        self.countryNames = []
        self.polygons = {}
        self.data = []
        self.polyCount = 0

        self.fileName = file_name
        self.loadFile()
        self.loadCountryPolys()

    def loadCountryPolys(self, file_name=None):
        if not file_name is None:
            self.loadFile(file_name)

        self.polyCount = 0
        for country in self.data:
            name = country["properties"]["name"]
            self.countryNames.append(name)
            self.polygons[name] = country

            # for poly in country["geometry"]["coordinates"]:
            #     if len(poly) == 1:
            #         self.polygons[name].append(
            #             {"id": self.polyCount, "coords": poly[0]}
            #         )
            #         self.polyCount += 1
            #     else:
            #         for subpoly in poly:
            #             self.polygons[name].append(
            #                 {"id": self.polyCount, "coords": subpoly}
            #             )
            #             self.polyCount += 1

    def loadFile(self, file_name=None):
        if not file_name:
            file_name = self.fileName
        else:
            self.fileName = file_name

        if not os.path.isfile(self.fileName):
            print(f"Error: File {self.fileName} doesn't seem to exist!!")
            sys.exit()

        with open(self.fileName) as f:
            self.data = json.load(f)

        if "features" in self.data:
            self.data = self.data["features"]

        elif not isinstance(self.data, list):
            print("Error? Is file correct format?")
            sys.exit()

    def getCountryIndex(self, name):
        """Finds the index (integer) of a country by name

        Args:
            name (string): name of a country

        Returns:
            mixed: Either integer index of a country or None

        Example:
            getCountryNameIndex("Poland")
            returns: 40
        """
        if name in self.countryNames:
            return self.countryNames.index(name)
        return None

    def getNames(self):
        return self.countryNames

    def getPolygons(self, country=None):
        if not country:
            return self.polygons

        if country in self.polygons:
            return self.polygons[country]


if __name__ == "__main__":
    europe = CountryReader("../data/Europe.geojson")

    print(europe.getNames())