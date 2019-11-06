# Functional Specification

The document should have the following sections:
* **Background** The problem being addressed.
* **User profile** Who uses the system. What they know about the domain and computing (e.g., can browse the web, can program in Python).
* **Data sources** What data you will use and how it is structured.
* **Use cases** Describing at least two use cases. For each, describe: (a) the objective of the user interaction (e.g., withdraw money from an ATM); and (b) the expected interactions between the user and your system.

## Background
* When moving to a new city/neighborhood, it is difficult to know the flow of traffic in the area.
  * Sites such as Zillow, Craigslist, etc., do not provide information about whether property is located near a busy street.
* This information may help movers make a decision on whether or not to buy a house in a particular location.
* **We will create an interactive mapping tool that provides users with information about vehicle and foot traffic for neighborhoods in Seattle.**
  * Users will be able to filter by neighborhood to discover foot and vehicle traffic flow.
  * Users will be able to view historical data about vehicle traffic flow.
  
## User profile

## Data sources
* [Seattle Streets](https://data-seattlecitygis.opendata.arcgis.com/datasets/seattle-streets)
  * GIS street data with street names, block numbers, and speed limit
* [2018 Traffic Flow Counts](https://data-seattlecitygis.opendata.arcgis.com/datasets/2018-traffic-flow-counts)
  * GIS traffic flow data with street names, average weekday traffic volume, and average day traffic volume
* [Seattle Neighborhoods](https://data.opendatasoft.com/explore/dataset/zillow-neighborhoods%40public/map/?refine.city=Seattle&location=10,47.6094,-122.33963&basemap=jawg.sunny)
  * GIS Seattle neighborhood data from Zillow

## Use cases
**Use case 1**: A user wants to view the vehicle traffic flow in a specific neighborhood
* User: Select the neighborhood from drop-down menu
  * App: Show all types of traffic flow in that neighborhood (e.g., bike, vehicle, foot)
* User: Click the checkbox for vehicle traffic flow
  * App: Filter by vehicle traffic flow
* User: Zoom in to see the blocks or street the user cares about
  * App: Show the traffic flow by width and/or color to indicate busy streets and blocks
  
**Use case 2**: A user wants to view the annual average weekday traffic flow in a neighborhood
* User: Select the neighborhood from drop-down menu
  * App: Show all types of traffic flow in that neighborhood (e.g., bike, vehicle, foot)
* User: Use slider on the top corner to choose a specific year
  * App: Show the traffic flow for a specific year on map
* User: Click the checkbox for Weekday
  * App: Show only the weekday traffic flow
* User: Choose View Report from the menu
  * App: Show statistics for annual average weekday traffic flow by different years
