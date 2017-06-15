import pandas as pd
import pprint as pp

# Chicago bike data
df = pd.read_csv('https://query.data.world/s/cj7k3r4opj9bxabl9hbft50kb')

pp.pprint(df)


# Ny crime data
df = pd.read_csv('https://query.data.world/s/1m9mvcgtcuat4bpkjhaisdfkm')