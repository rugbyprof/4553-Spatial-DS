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

- ***Query 1: Find Interesting Features along some path:***
    - Select a starting point: `X` and a destination point `Y`. This can be done by mouse click, or by entering airport codes via `sys.argv` (e.g. `python query1.py DFW MNL 500` to run query from Dallas / Fort Worth to Manilla Philippines with a 500 mile radius to look for interesting features).
    - Determine a milti-line path between `X & Y`, and draw an appropriate line connecting each point.
    - Highlight all features within `R` radius of the entire path by showing volcanos as red dots, earthquakes as blue dots, and meteor locations as green dots.
    - Assume that each line segment cannot be more than 500 miles long, meaning you must find an airport within a 500 mile radius of each stop. Choose the largest airport at each stop (e.g. where `ap_level` is the lowest value) and if there are more than one airport with the same `ap_level`, choose the airport at the lowest `elevation` as a tie breaker.
    - An example `X` and `Y` might be `Dallas, U.S.` to `Manila, Philippines` with a 500 mile radius.
    - Which way do you fly to start? East or West?
    
    
- ***Query 2: Nearest Neighbor:*** 
    - Click on the world map and get the nearest `feature` within `XXX` miles, possibly with specific feature values, further filtering the query (magnitude of earthquake, etc.) where `features` are listed below:
        - Volcanos 
        - Earthquakes 
        - Meteors
    - Example queries may be:
        - `python query2.py [feature] [field] [field value] [min/max] [max results] [radius] [lon,lat]`
            - ***feature*** = volcano, earthquake, meteor
            - ***field*** = some field in the 'properties' to compare against
            - ***field_value*** = the value in wich to compare with
            - ***min/max*** = whether we want all results greater than or less than the field_value.
            - ***radius*** (in miles) = radius to apply our query with.
            - ***lon,lat*** (optional) = Some point coords to act as a mouse click instead of actually clicking the screen. If these exist when query2.py is run, then it should just perform the query with the given point and not wait on a mouse click.
        - `python query2.py volcanos altitude 3000 min 3 1000` When the map is clicked it will find the 3 volcanos within a 1000 mile radius that are at a minumum of 3000 feet (if they exist at that location).
        - `python query2.py earthquakes magnitude 5 min 0 2000` When the map is clicked it will find ALL earthquakes (max results 0 = all) within a 2000 mile radius with a magnitude of 5 or more. 
        - `python query2.py 1000` This query if rum with a single parameter, you will assume it is a Radius and you should find ALL of the above features within that radius (Volcanos, Earthquakes, Meteors). Only display the first 500 results if there are any performance issues. 
        - Show volcanos as red dots, earthquakes as blue dots, and meteor locations as green dots.
        
- ***Query 3: Clustering:***
    - Use dbscan to find the top 3-5 clusters of volcanoes, earthquakes, and meteors. 
    - If combining all of the data points is hard, get the biggest cluster from each data type seperately.
    - Draw a bounding box around each cluster.
    - Example Usage may be:
        - `python query3.py [feature] [min_pts] [eps]` 
            - ***Feature*** = (volcano, earthquake, meteor) and 
            - ***min_pts*** = minimum points to make a cluster, and 
            - ***eps*** is the distance parameter for dbscan
        - `python query3.py [feature] [min_pts] [eps]`
  
    
### Deliverables
- Place all necessary files in your `program_5` folder.
- This includes any documents from `part 1` as well as any files necessary to make your programs run within this folder to include:
    - Your geoJson files from `program_4`.
    - The batch file to load these files into pymongo.
    - A `README.md` that describes what someone would need to do to make your code run. For example:
        - The name of your mongo db, and collections.
        - How to run your batch file.
        - Some example queries for each `queryX.py` and NOT my examples. Chooses params that you feel confident will run correctly.
- Make sure that your ideas from part one are in a file called: `query_ideas.md` 
- Make sure that your screen shot is in this folder in a file called `pymongo_proof.xxx` (where xxx is whatever format you saved your screenshot in.
- Place each of your `Queries` in files called:
    - query1.py
    - query2.py
    - query3.py
- and that each of these files runs based on the "usage" described. If there are any issues whith my logic (it's currently ~0248~ 0301 am) then let me know. I tried to make the usage as un-ambiguous as I could without having a ton of parameters, but I may not have succeeded. 
- Were also NOT trying to make the usage exremely robust. For example, I don't care about earthquakes less than magnitude of 3ish, so I'm not truly worried about the 'max' param working for earthquake as well some others. If your confused, ask in class. 
- NO query is expected to run more than once. Meaning, one set of input params, or one mouse click. If you want to clear the screen on subsequent clicks to re-run, thats optional.

