import pprint as pp
import os,sys

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))

keys = []
crimes = []

got_keys = False
#with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:
with open(DIRPATH+'/'+'nypd_small_data.txt') as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
        line = line.strip().split(',')
        if not got_keys:
            keys = line
            print(keys)
            got_keys = True
            continue

        #d = {}
        # for i in range(len(line)-1):
        #     d[keys[i]] = line[i]
        crimes.append(line)
for crime in crimes:
    print(crime[19],crime[20])