# Component Specification

<!---
The document should have sections for:
* **Software components** High level description of the software components such as: *data manager*, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and *visualization manager*, which displays data frames as a plot. Describe at least 3 components specifying what it does, inputs it requires, and outputs it provides.
* **Interactions to accomplish use cases** Describe how the above software components interact to accomplish at least one of your use cases.
* **Preliminary plan** A list of tasks in priority order.
--->

## Software Components
* **Layout manager**: HTML structure of dashboard
    * Includes HTML headers and divs for map, chart, and interactive components
    * Input: Dictionary of map data and chart data, current state of interactive components
    * Output: Dashboard displays in browser
* **Map manager**: Plotly map
    * Display either neighborhood polygons or street-level traffic flow for specific neighborhood
    * Input: Filtered Pandas DataFrame from data manager
    * Output: Dictionary of updated map data to layout manager
* **Chart manager**: Plotly charts
    * Display statistical charts (e.g., time series, histograms, etc.) for traffic flow trends
    * Input: Filtered Pandas DataFrame from data manager
    * Output: Dictionary of updated chart data to layouy manager
* **Callback managers**:
    * Control interactions and current state
    * Input: User hovers, clicks, drop-down selections, and slider changes
    * Output: Current neighborhood, time of day, and year to data manager
* **Data manager**: 
    * Load street, neighborhood, and traffic flow data
    * Join data by neighborhood and street
    * Query data for neighborhood, time of day, and year
    * Input: Current neighborhood, time of day, year from callback managers
    * Output: Filtered Pandas dataframe to map and chart managers

## Interactions
* **Hover**: Hover mouse over neighborhood or street to view name and traffic flow
* **Click**: Click on neighborhood to zoom in on map and display street-level traffic flow
* **Drop-down menu**: Select neighborhood to zoom in on map and display street-level traffic flow
* **Checkboxes**: Select time of day (AM Peak, PM Peak, Weekday, Daily)
* **Slider**: Select year (2007-2018)
* **Button**: Generate statistical charts

## Preliminary Plan
1. Create dashboard template, including HTML divs for map, chart, and interactive components
2. Create function to load and join datasets
3. Create functions to display neighborhood map and traffic flow map
4: Create functions to display statistical charts
4. Create callback functions for interactive components
5. Create function to filter dataset based on current state
