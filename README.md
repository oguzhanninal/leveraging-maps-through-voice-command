## Display military movements on a map
#### The Wizards of Doz

App using Leaflet and Flask to display important troops and military movements on a map.

A map of Europe centered on Germany is displayed on the UI. 

### Audio Recording
- Record button uses JavaScript [MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) to receive audio from the user's device microphone.
- Makes a Post request to Flask App to save the recorded audio.
- Audio is transcribed using OpenAI Whisper and saved to the instruction log to be displayed.

### Instruction Processing
- The get_string Flask route reads the most recent instruction from the intruction log
- Sends it to the Open AI instance to encode user's natural language instruction as a json object 
- That json is passed to the generate positions function
- Generate Positions creates a list of vectors that are closely aligned with the appropriate shape file based on the user's instructions: roads, rail, or rivers.
- A polyline is shown on the map that conforms to the user's instructions.

For Example, if the user says "Tank movements spotted on the road from Hanover to Bergen".

ChatGPT is prompted to turn this into an object of the following form:

`
{'Object_Type' : 'Tank',
    'StartLat': 52.3759,
    'StartLong': 9.7320,
    'EndLat': 52.8114,
    'EndLong': 9.9632,
    }
   `
This object is passed to the generate_pos function to generate the positions.

###  Position generations
We start by importing shapefiles (`.shp`) using GeoPandas to extract road network geometries. These are converted into a `networkx` graph:
- GeoDataFrame to Graph:
  - Shapefiles are read using `gpd.read_file()`.
  - Road geometries (typically LineStrings) are parsed and each segment becomes an edge in a directed graph.
  - Nodes are created from the start and end coordinates of each road segment.
  - Graph edges are enriched with attributes like `length`, `geometry`, and travel time estimation.

Network Routing with NetworkX + SimPy
- Shortest Path Routing:
  - Using `nx.shortest_path()` to find optimal routes between origin and destination points based on edge weights.
- Simulation with SimPy:
  - SimPy is used to simulate vehicle agents navigating the graph from point A to B.
  - Vehicles yield timeouts based on travel time per segment.
  - A log dictionary is created, storing each vehicle's path and timing for later use.


## UI 
Is a basic html template. Some buttons are not implemented (see below)

### Not yet implemented
* Single loop from recording to showing lines on the map. Currently, one step is required to log the instructions, and a second step is required to display the results.
* Functionality to show all given instructions on the map or clear what has been there
* Functionality to display the data recorded from the last function

  