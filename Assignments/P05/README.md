## Worldle - Spatial Game Api
#### Due: 04-26-2022 (Tuesday @ 9:30 a.m.)


### Overview

- Using `FastApi` as a library, write a backend api that can be used to assist your game into becoming a reality. 
- Starter code can be found here: [Lectures/09_ApiHelp](../../Lectures/09_ApiHelp/)


### Api
- Create routes that do the following:
  - Gets a single polygon from the countries geojson data, the polygon that best represents the countries border.
  - Get a list of country names that could be used to display to a user.
  - Get a list of country "suggestions" as determined by a partial string match to a key value sent from the user.
  - Get a point that represents the center of a polygon to help in a distance calculation between countries.
  - Get the distance between:
    - Two points
    - Two polygons (implemented preferably as discussed in class)
  - Get a hint from the api (returns the "continent" that the goal country resides on (in?)). 
  - Any other routes you may need to help run the game.


### Deliverables

- Create a folder called `P05` in your `assignments` folder on your repo.
- Add your files that contain your "api" with a number of "tests" written to show the code works. 
- Create a readme in `P05` with a small write up describing your module. 
- Please refer to the [Readmees](../../Resources/02-Readmees/README.md) folder for help on creating a worthwhile readme.

