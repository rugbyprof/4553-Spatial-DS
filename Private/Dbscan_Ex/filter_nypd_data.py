import pprint as pp

categories = "LARCENY ASSAULT HARRASSMENT DRUGS VEHICLE FRAUD".split(' ')
files = "Nypd_Crime_01.csv Nypd_Crime_02.csv Nypd_Crime_03.csv Nypd_Crime_04.csv".split(' ')
data_folder = "/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/"
boros = "BRONX BROOKLYN MANHATTAN QUEENS STATEN_ISLAND".split(' ')
chunks = {}
chunks2 = {}

def keep_record(OFNS_DESC,BORO_NM,b):

    words = OFNS_DESC.split(' ')
    boro = BORO_NM.strip().replace(" ", "_")
    for cat in categories:
        if cat in words and b == boro:
            return cat
    return None

def process_data_file(file_name,b):
    global chunks
    global chunks2
 
    with open(file_name) as f:
        for line in f:
            # fix line by replacing commas in between double quotes with colons
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            # turn line into a list
            sline = line.strip().split(',')
            cat = keep_record(sline[7],sline[13],b)
            if cat is not None:
                if b not in chunks:
                    chunks[b] = {}
                if cat not in chunks[b]:
                    chunks[b][cat] = []
                chunks[b][cat].append(line)
                if cat not in chunks2:
                    chunks2[cat] = {}
                if b not in chunks2[cat]:
                    chunks2[cat][b] = []
                chunks2[cat][b].append(line)


for f in files:
    for b in boros:
        process_data_file(data_folder+f,b.strip())

# for burough, d in chunks.items():
#     print(burough)
#     for crime, rows in d.items():
#         f = open(data_folder+burough.title()+"_"+crime.title()+".csv","w")
#         for r in rows:
#             f.write(r)
#         print(f)
#         print(crime)
#         print(len(rows))

for crime, d in chunks2.items():
    print(crime)
    for burough, rows in d.items():
        f = open(data_folder+crime.title()+"_"+burough.title()+".csv","w")
        for r in rows:
            f.write(r)
        print(f)
        print(crime)
        print(len(rows))