Program 5 - PyMongo
=========

### Due: Mon Jul 3rd by Classtime

![](https://d3vv6lp55qjaqc.cloudfront.net/items/3f2W3H0N2h3H11402t3a/1024x512_cropped.png) 

## Part 1

### Requirements
- RUN pymongo!!

### Deliverables
- Create a folder called `program_5` in your assignments folder.
- Include any pymongo code that runs on YOUR system.
- Create a screen shot showing your file running on YOUR system.
- Upload both file and screenshot to your assignments folder. 
- Upload a document that has a minimum of 3 ideas for queries.

## Part 2

- Query 1: Find Interesting Features along some path:
    - Select a starting point: `X` and a destination point `Y`. This can be done by mouse click, or by entering airport codes via `sys.argv` (e.g. `python query1.py DFW MNL` to run query from Dallas / Fort Worth to Manilla Philippines).
    - Determine a milti-line path between `X & Y`, and draw an appropriate line connecting each point.
    - Highlight all features with `R` radius of the entire path by showing volcanos as red dots, prior earthquakes as blue dots, and meteor locations as green dots.
    - Assume that `X` and `Y` are NOT on the same continent.
    - Assume that each line segment cannot be more than 500 miles long, meaning you must find an airport within a 500 mile radius of each stop. Choose the largest airport at each stop (e.g. where `ap_level` is the lowest value) and if there are more than one airport with the same `ap_level`, choose the airport at the lowest `elevation` as a tie breaker.
    - An example `X` and `Y` might be `Dallas, U.S.` to `Manila, Philippines`
    - Which way do you fly? East or West?
    
    
- Query 2: Nearest Neighbor: 
    - Click on the world map and get the nearest `______________` within `XXX` miles, possibly with specific features further filtering the query (magnitude of earthquake, etc.) 
        1. Cities 
        2. Volcanos 
        3. Earthquakes 
        4. Airports
        
        
- Query 3: Clustering:
    - Use clustering to find the top 5 clusters of volcanoes and/or earthquakes. 
    - Query to find which city is most central to each cluster. 
    - Route through airports from some origin, `X` to a destination, `Y` so that each cluster is visited and then return back to the place of origin. 
    
### Deliverables
- Place all necessary files in your `program_5` folder.
- This includes any documents from `part 1` as well as any files necessary to make your programs run within this folder to include:
    - Your geoJson files from `program_4`.
    - The batch file to load these files into pymongo.
    - A `README.md` that describes what someone would need to do to make your code run. For example:
        - The name of your mongo db, and collections.
        - How to run your batch file.
- Make sure that your ideas from part one are in a file called: `query_ideas.md` 
- Make sure that your screen shot is in this folder in a file called `pymongo_proof.xxx` (where xxx is whatever format you saved your screenshot in.
- Place each of your `Queries` in files called:
    - query1.py
    - query2.py
    - query3.py

