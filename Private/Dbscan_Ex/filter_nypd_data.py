

categories = "LARCENY ASSAULT HARRASSMENT DRUGS VEHICLE FRAUD".split(' ')
files = "Nypd_Crime_01.csv Nypd_Crime_02.csv Nypd_Crime_03.csv Nypd_Crime_04.csv".split(' ')
data_folder = "/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/"
boros = "BRONX BROOKLYN MANHATTAN QUEENS STATEN_ISLAND".split(' ')

keys = []
count_rows = {}
got_keys = False

def keep_record(OFNS_DESC,BORO_NM,b):

    words = OFNS_DESC.split(' ')
    boro = BORO_NM.strip().replace(" ", "_")
    for word in words:
        if word in categories and b == boro:
            if word not in count_rows:
                count_rows[word] = 0
            count_rows[word] += 1
            return True
    return False

def process_data_file(file_name,b):
    global got_keys
    filtered = open('/code/repos/4553-Spatial-DS/Private/Dbscan_Ex/filtered_crimes_'+ b.lower() +'.csv','a')

    data = []
    with open(file_name) as f:
        for line in f:
            # fix line by replacing commas in between double quotes with colons
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            # turn line into a list
            sline = line.strip().split(',')
            if not got_keys:
                keys = line
                got_keys = True
                filtered.write(line)
                continue
            if keep_record(sline[7],sline[13],b):
                filtered.write(line)

    return data


print(categories)
print(files)
data = []

for f in files:
    print("Processing: %s" % (data_folder+f))
    for b in boros:
        print("Boro: %s" % (b))

        data.extend(process_data_file(data_folder+f,b.strip()))
        print("Size: %d" % len(data))
