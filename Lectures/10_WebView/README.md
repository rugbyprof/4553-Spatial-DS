## Introduction to Web Mapping
#### Michael Dorman

### Tutorial

- Nice intro to web / geoJson viewing with OpenStreet Maps and LeafLet Js: 
  - [http://132.72.155.230:3838/js/index.html](http://132.72.155.230:3838/js/index.html)

### Live Server Extension

- Need the "Go Live" Extension from VSCode ... 

### Examples

The examples are based on the tutorial linked to above. I tried to add functionality in a somewhat logical manner. As more javascript is added (the code in the script tags), like in 06 and 07, there is definitely room for improvement. For example the functions I added that make api requests, definitely have a lot of repeat code and could be combined. Which, as I'm writing this I decided to add an 08 to fix those issues

- [01-basic_js.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/01_basic_js.html)
  - Shows a simple point added to an open street maps "tile layer". 
- [02-basic_map.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/02_basic_map.html)
  - Shows two states with generic styling. 
- [03_basic_style.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/03_basic_style.html) 
  - Shows two states with same default styling defined by dev. 
- [04_basic_styleV2.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/04_basic_styleV2.html) 
  - Shows two states with different styles using a style function.
- [05_load_geo.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/05_load_geo.html) 
  - Shows a geoJson object on the map after pasted and submitted.
- [06_api_caller.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/06_api_caller.html)  
  - Calls api to get country names, then displays country on map after chosen on web page.
- [07_api_caller_V2.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/07_api_caller_V2.html)  
  - Same as 06 but when country selected, it pans to the new country and zooms in.
- [08_cleaner_api_caller.html](https://github.com/rugbyprof/4553-Spatial-DS/blob/master/Lectures/10_WebView/08_cleaner_api_caller.html)  
  - Same as 07 but cleaned up syntax with duplicate code combined into functions.  
  - Added a "table" to show a "history" of countries chosen.
  - Necessary css added to make table look decent.


https://blog.logrocket.com/localstorage-javascript-complete-guide/