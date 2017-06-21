f = open('/code/repos/4553-Spatial-DS/Resources/Data/WorldData/cities1000.txt','r')

data = f.read()

data = data.split("\n")

new = []

for d in data:
    new.append(d.split("\t"))
    print(new[-1][2],new[-1][4],new[-1][5],new[-1][8],new[-1][-2])