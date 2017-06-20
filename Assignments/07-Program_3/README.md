Program 3 - DBscan - Earthquake Data
=========

### Due: Thu Jun 22nd by Classtime

### Overview

- Start code can be found [HERE](https://github.com/rugbyprof/4553-Spatial-DS/tree/master/Resources/Program_3_Starter) 
- Were not going to cluster these points. 
- Create a json file with all the earthquakes that have a magnitude 7 and greater from the year 1960-2016.
- Using pygameto display each point representing an earthquake. Use a color that is easy to see.
- Add a background image to your output that is 1024x512. Here is one you can use (thank Nash):

![](https://api.mapbox.com/styles/v1/mapbox/dark-v9/static/0,0,1/1024x512?access_token=pk.eyJ1IjoiY29kaW5ndHJhaW4iLCJhIjoiY2l6MGl4bXhsMDRpNzJxcDh0a2NhNDExbCJ9.awIfnl6ngyHoB3Xztkzarw) 

- This is a code snippet to add a background image.
```python
# Put this after pygame.init()
bg = pygame.image.load("path/to/image.png")

# Put this in your game loop:
screen.blit(bg, (0, 0))
```

- Make sure you do a screen shot of your output: `pygame.image.save(screen,DIRPATH+'/'+'screen_shot.png')`
- Extra credit if anyone can make the earthquakes appear a year at a time in an additive manner.
- Extra credit if you want to show clusters. 

### Deliverables

- Create a folder called program 3.
- Put your code in `main.py` in your program_3 folder.
- Create a screen shot of your output and turn that in at the beginning of class Thursday with a print out of your `main.py`
- Include any data files you used in your program_3 folder.
- Ensure everything is on github.


