# Functional Specification

<!---
The document should have the following sections:
* **Background** The problem being addressed.
* **User profile** Who uses the system. What they know about the domain and computing (e.g., can browse the web, can program in Python).
* **Data sources** What data you will use and how it is structured.
* **Use cases** Describing at least two use cases. For each, describe: (a) the objective of the user interaction (e.g., withdraw money from an ATM); and (b) the expected interactions between the user and your system.
--->

## Background
Traffic flow is an important feature to consider when moving to a new city. Unfortunately, sites such as Zillow, Craigslist, etc., may not provide information about the traffic flow near a particular property. To help people moving to Seattle, we will create an interactive dashboard that allows users to explore traffic flow trends in Seattle neighborhoods.
  
## User profile
Users are anyone interested in learning more about traffic flow in Seattle neighborhoods. Should be familiar with web browser interactions such as hover, click, select from drop-down menu, etc. Must be able to clone a git repository and run a Python script. 

## Data sources
* [Seattle Streets](https://data-seattlecitygis.opendata.arcgis.com/datasets/seattle-streets)
  * GIS street data with street names, block numbers, and speed limit
* [2018 Traffic Flow Counts](https://data-seattlecitygis.opendata.arcgis.com/datasets/2018-traffic-flow-counts)
  * GIS traffic flow data with street names, average weekday traffic volume, and average daily traffic volume
  * Datasets also available for 2007-2017
* [Seattle Neighborhoods](https://data.opendatasoft.com/explore/dataset/zillow-neighborhoods%40public/map/?refine.city=Seattle&location=10,47.6094,-122.33963&basemap=jawg.sunny)
  * GIS Seattle neighborhood data from Zillow

## Use cases
**Use case 1**: User wants to view recent traffic flow in a specific neighborhood
* User: Select neighborhood in drop-down menu or click on neighborhood in map
    * Dashboard: Zoom in on neighborhood in map and display streets colored by 2018 average daily traffic flow
* User: Hover mouse over specific street
   * Dashboard: Display street name and traffic flow counts
   
**Use case 2**: User wants to traffic flow by time of day in a specific neighborhood
* User: Select neighborhood in drop-down menu or click on neighborhood in map
    * Dashboard: Zoom in on neighborhood in map and display streets colored by 2018 average daily traffic flow
* User: Click checkbox for AM Peak, PM Peak, Weekday, or Daily
   * Dashboard: Display streets colored by traffic flow for selected time

**Use case 3**: User wants to view traffic flow trends in a specific neighborhood
* User: Select neighborhood in drop-down menu or click on neighborhood in map
   * Dashboard: Zoom in on neighborhood in map and display streets colored by 2018 average daily traffic flow
* User: Use slider to change year
   * Dashboard: Display streets colored by traffic flow for selected year
 
**Use case 4**: User wants to view traffic flow statistics for specific neighborhood
* User: Select neighborhood in drop-down menu or click on neighborhood in map
    * Zoom in on neighborhood in map and display streets colored by 2018 average daily traffic flow
* User: Click View Report
    * Dashboard: Display various charts (e.g., time series, histograms, etc.) for neighborhood traffic flow
