/**
 * eventFire
 *
 * This method is used to fire an even on another html (dom) element.
 * For example it can be used to click a button, based on another action
 *
 *Example: simulate a click on the map.
 *
 *    eventFire(document.getElementById('map'), 'click');
 *
 * @param el - element to fire even on
 * @param etype - event type to fire
 */
function eventFire(el, etype) {
   if (el.fireEvent) {
      (el.fireEvent('on' + etype));
   } else {
      var evObj = document.createEvent('Events');
      evObj.initEvent(etype, true, false);
      el.dispatchEvent(evObj);
   }
}

var reqAnimFrame = window.requestAnimationFrame ||
   window.mozRequestAnimationFrame ||
   window.webkitRequestAnimationFrame;


// Create an instance of pantograph.
// In javascript, this is one way to create an object.
var pantograph = {};

//This is my access token for mapbox
//The L object exists because we included `mapbox.js` in the html template.
L.mapbox.accessToken =
   'pk.eyJ1IjoicnVnYnlwcm9mIiwiYSI6ImNpZ3M1aDZwbzAyMnF1c20xcnM4ZGowYWQifQ.s6ghscOu98he230FV1_72w';

//Any variable that starts with `pantograph` belongs to the pantograph "class".
//I didn't write all this code, so I'm not 100% clear on all of them.

//Socket to pass info back and forth to `handler.py`
pantograph.socket = new WebSocket(ws_url);

//This is the reference to the "canvas" in the html page
pantograph.context = canvas.getContext("2d");

//This creates the canvas in the html page by finding the element tag <canvas>
pantograph.hiddenCanvas = document.createElement("canvas");

//Sets local references to the width and height of the canvas
pantograph.hiddenCanvas.width = canvas.width;
pantograph.hiddenCanvas.height = canvas.height;

//So we "created" a canvas obove (pantograph.hiddenCanvas), now we need to
//reference the "context" or current state.
pantograph.hiddenContext = pantograph.hiddenCanvas.getContext("2d");

//Sends messages back to `handler.py` based on events
pantograph.input_handler = function(e) {
   var ws = pantograph.socket;
   var message = {
      type: e.type || "",
      x: e.offsetX || 0,
      y: e.offsetY || 0,
      button: e.button || 0,
      alt_key: e.altKey || false,
      ctrl_key: e.ctrlKey || false,
      meta_key: e.metaKey || false,
      shift_key: e.shiftKey || false,
      key_code: e.keyCode || 0
   }
   ws.send(JSON.stringify(message));
   console.log(JSON.stringify(message));
}



// Redraws the canvas
pantograph.redrawCanvas = function(mess, operation) {
   var ctx = pantograph.context;
   var hidCtx = pantograph.hiddenContext;
   var hidCvs = pantograph.hiddenCanvas;

   reqAnimFrame(function() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(hidCvs, 0, 0);
   });
}

// Clear area by drawing a rectangle.
pantograph.clearRect = function(ctx, rect) {
   ctx.clearRect(rect.x, rect.y, rect.width, rect.height);
}

/**
 * Drawing methods
 *
 * Each method does bascially the same thing:
 *
 * 1. Gets a reference to the context (ctx) of the canvas
 * 2. Draws the shape.
 *    2a. Stroke usually means line or outline
 *    2b. Fill usually means ... well ... fill with a color
 * 3. Add the shape to the ctx.
 */

pantograph.drawRect = function(ctx, rect) {
   if (rect.lineColor) {
      ctx.strokeStyle = rect.lineColor;
      ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
   }
   if (rect.fillColor) {
      ctx.fillStyle = rect.fillColor;
      ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
   }
}


pantograph.drawCircle = function(ctx, circle) {
   ctx.beginPath();
   ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI, true);
   if (circle.lineColor) {
      ctx.strokeStyle = circle.lineColor;
      ctx.stroke();
   }
   if (circle.fillColor) {
      ctx.fillStyle = circle.fillColor;
      ctx.fill();
   }
}

pantograph.drawOval = function(ctx, oval) {
   var x = oval.x + oval.width / 2;
   var y = oval.y + oval.height / 2;

   ctx.save();
   ctx.translate(x, y);

   ctx.scale(oval.width, oval.height);

   ctx.beginPath();
   ctx.arc(0, 0, 0.5, 0, 2 * Math.PI, true);

   ctx.restore();

   if (oval.lineColor) {
      ctx.strokeStyle = oval.lineColor;
      ctx.stroke();
   }

   if (oval.fillColor) {
      ctx.fillStyle = oval.fillColor;
      ctx.fill();
   }
}

pantograph.drawLine = function(ctx, line) {
   ctx.beginPath();
   ctx.moveTo(line.startX, line.startY);
   ctx.lineTo(line.endX, line.endY);
   ctx.strokeStyle = line.color || "#000";
   ctx.stroke();
}

pantograph.drawPolygon = function(ctx, polygon) {
   var startX = polygon.points[0][0];
   var startY = polygon.points[0][1];

   ctx.beginPath();
   ctx.moveTo(startX, startY);

   polygon.points.slice(1).forEach(function(pt) {
      ctx.lineTo(pt[0], pt[1]);
   });

   ctx.lineTo(startX, startY);

   if (polygon.lineColor) {
      ctx.strokeStyle = polygon.lineColor;
      ctx.stroke();
   }

   if (polygon.fillColor) {
      ctx.fillStyle = polygon.fillColor;
      ctx.fill();
   }
}

pantograph.drawImage = function(ctx, imgInfo) {
   var img = new Image();
   img.src = imgInfo.src;

   var width = imgInfo.width || img.width;
   var height = imgInfo.height || img.height;

   ctx.drawImage(img, imgInfo.x, imgInfo.y, width, height);
}

pantograph.drawCompound = function(ctx, compound) {
   compound.shapes.forEach(function(shp) {
      pantograph.shapeToFunc[shp["type"]](ctx, shp);
   });
}


/**
 * This is a lookup for which function to call based on the name
 * of the shape passed in by `message`
 */
pantograph.shapeToFunc = {
   clear: pantograph.clearRect,
   rect: pantograph.drawRect,
   oval: pantograph.drawOval,
   circle: pantograph.drawCircle,
   image: pantograph.drawImage,
   line: pantograph.drawLine,
   polygon: pantograph.drawPolygon,
   compound: pantograph.drawCompound
}

// A generic function that draws a shape based on some json input.
// It needs to be down here, so any function it trys to call will
// be defined before it.
pantograph.drawShape = function(shape) {
   var ctx = pantograph.hiddenContext;

   // Decide which shape to draw by getting the "type" then calling "shapeToFunc"
   var operation = pantograph.shapeToFunc[shape["type"]];

   //Print error if needed
   if (operation === undefined) {
      console.log("Could not find operation for shape " + shape["type"]);
   }

   // Put the shape on the canvas
   reqAnimFrame(function() {
      ctx.save();
      if (shape.rotate) {
         ctx.translate(shape.rotate.x, shape.rotate.y);
         ctx.rotate(shape.rotate.theta);
         ctx.translate(-shape.rotate.x, -shape.rotate.y);
      }
      operation(ctx, shape);
      ctx.restore();
   });
}

/**
 * This sets all the listeners to look out for whether
 * it's on the canvas or document body. If an event happens
 * it sends it to `input_handler` which sends it to `handlers.py`
 */
pantograph.socket.onopen = function(e) {

   //This is a reference to the drawing canvas and sends any
   canvas.onmousedown = pantograph.input_handler;
   canvas.onmouseup = pantograph.input_handler;
   canvas.onmousemove = pantograph.input_handler;
   canvas.onclick = pantograph.input_handler;
   canvas.ondblclick = pantograph.input_handler;

   //These reference the entire document body listening for keystrokes
   document.body.onkeydown = pantograph.input_handler;
   document.body.onkeyup = pantograph.input_handler;
   document.body.onkeypress = pantograph.input_handler;

   pantograph.socket.send(JSON.stringify({
      type: "setbounds",
      width: canvas.width,
      height: canvas.height
   }));
}

/**
 * NOT USED YET
 */
pantograph.panMap = function(mapInfo) {
   console.log(mapInfo);
   console.log(pantograph.map.getCenter())
   bounds = pantograph.map.getPixelBounds()
   console.log(bounds.max.x - bounds.min.x)
   console.log(bounds.max.y - bounds.min.y)
   console.log(pantograph.map.getPixelOrigin())
}


/**
 * Was used to simulate a map click but doesn't work. well
 * it does attempt to click the "map" but it's undefined.
 */
pantograph.clickMap = function(mapInfo) {
   //eventFire(document.getElementById('map'), 'click');
}


/**
 * This gets my map from mapbox and sets the initial view with zoom
 */
pantograph.initMap = function(mapInfo) {
   pantograph.map = L.mapbox.map('map', 'rugbyprof.o4e374ki').setView([
      mapInfo.lat, mapInfo.lon
   ], mapInfo.zoom);

   //This adds a "listen" for click event to happen (on the map)
   pantograph.map.on('click', function(e) {
      console.log(e.latlng); // e is an event object (MouseEvent in this case)

   });
}

/**
 * Hides the loading graphic that shows while the shape file is being
 * loaded.
 */
pantograph.hideMapLoader = function() {
   document.getElementById("loader").style.display = "none";
   console.log(document.getElementById("loader"));
}


/**
 * This zooms in to the extent of the shape file, really just finding
 * the closest zoom level that fits all the points.
 */
pantograph.fitBounds = function(data) {
   console.log(data)
   pantograph.map.fitBounds(
      [
         [data.minLat, data.minLon],
         [data.maxLat, data.maxLon]
      ]
   )

   //Temp stuff
   console.log(pantograph.map.getBounds());
   console.log(pantograph.map.getSize());
   console.log(pantograph.map.getPixelBounds());
   console.log(pantograph.map.getPixelOrigin());
}

/**
 * This handles the messages coming from `handlers.py`. Basically any
 * time you see a `self.do_operation()` in handlers.py, it's coming
 * here to get handled. 
 */
pantograph.socket.onmessage = function(e) {
   message = JSON.parse(e.data);
   if (message.operation == "refresh") {
      pantograph.redrawCanvas();
   } else if (message.operation == "panMap") {
      pantograph.panMap(message);
   } else if (message.operation == "draw") {
      pantograph.drawShape(message["shape"]);
   } else if (message.operation == "initMap") {
      pantograph.initMap(message);
   } else if (message.operation == "hideMapLoader") {
      pantograph.hideMapLoader();
   } else if (message.operation == "fitBounds") {
      pantograph.fitBounds(message);
   } else if (message.operation == "clickMap") {
      pantograph.clickMap(message);
   }
}
