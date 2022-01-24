""" This isn't really "fixing" the data files. It's really breaking them. Sorry. 
    Getting rid of "rank" and shuffling the cities to make sure they are un-ordered.
"""


# These lines let me change my working directory. I only use this when I'm
# using VSCode and the base directory isn't where I'm running scripts.
# This will error if you run it on repl.it or on your computer (unless you have
# the exact same path as below.) You can comment it out, or delete it. 
import os
os.chdir("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data")



from random import shuffle
import json

def shuffleJsonFile():

    with open("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/cities_latlon_w_pop.json") as f:
        data = json.load(f)

    for item in data:
        del item["rank"]

    shuffle(data)
    #print(data)

    with open("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/cities_latlon_w_pop2.json" , "w") as f:
        json.dump(data,f,indent=4)

    headers = list(data[0].keys())
    with open("/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Resources/01_Data/cities_latlon_w_pop2.csv" , "w") as f:
        f.write(",".join(headers))
        f.write("\n")
        for item in data:
            print(list(item.values()))
            v = list(item.values())
            v = [str(x) for x in v]
            print(v)
            f.write(",".join(v))
            f.write("\n")





if __name__=='__main__':
    shuffleJsonFile()
    #shuffleCsvFile()