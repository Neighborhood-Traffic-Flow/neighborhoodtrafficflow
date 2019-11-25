# Component Specification

<!---
The document should have sections for:
* **Software components** High level description of the software components such as: *data manager*, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and *visualization manager*, which displays data frames as a plot. Describe at least 3 components specifying what it does, inputs it requires, and outputs it provides.
* **Interactions to accomplish use cases** Describe how the above software components interact to accomplish at least one of your use cases.
* **Preliminary plan** A list of tasks in priority order.
--->

## Software Components
* **Layout manager**: HTML structure of dashboard
    * What it does: Includes HTML headers and divs for map, chart, and interactive components
    * Input: Dictionary of map data and chart data, current state of interactive components
    * Output: Dashboard displays in browser
* **Callback manager**:
    * What it does: Control interactions and current state
    * Input: User hovers, clicks, drop-down selections, and slider changes
    * Output: Current neighborhood, time of day, and year to data manager
* **Data manager**: 
    * What it does: - Load street, neighborhood, and traffic flow data
    *               - Join data by neighborhood and street
    *               - Query data for neighborhood, time of day, and year
    * Input: Current neighborhood, time of day, year from callback managers
    * Output: Filtered Pandas dataframe to map and chart managers
* **Map manager**: Plotly map
    * What it does: Display either neighborhood polygons or street-level traffic flow for specific neighborhood
    * Input: Filtered Pandas DataFrame from data manager
    * Output: Dictionary of updated map data to layout manager
* **Chart manager**: Plotly charts
    * What it does: Display statistical charts (e.g., time series, histograms, etc.) for traffic flow trends
    * Input: Filtered Pandas DataFrame from data manager
    * Output: Dictionary of updated chart data to layouy manager


## Interactions
* **Hover**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on hovers 
    * Data manager that loads street, neighborhood, and traffic flow data
    * Map manager that displays neighborhood or street for specific neighborhood on map
    * Control logic
* **Click**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on clickers 
    * Data manager that loads street, neighborhood, and traffic flow datathat and joins data by neighborhood and street 
    * Map manager that displays zoom-ins and street-level traffic flow
    * Control logic
* **Drop-down menu**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on drop-down selections
    * Data manager that loads street, neighborhood, and traffic flow data for selected neighborhood
    * Map manager that displays zoom-ins and street-level traffic flow for selected neighborhood
    * Control logic
* **Checkboxes**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on checkboxes 
    * Data manager that selects time of day (AM Peak, PM Peak, Weekday, Daily)
    * Map manager that displays street-level traffic flow for selected time of day (AM Peak, PM Peak, Weekday, Daily)
    * Control logic 
* **Slider**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on sliders
    * Data manager that selects the specific year (e.g. 2007-2018)
    * Map manager that displays street-level traffic flow for selected year (e.g. 2007-2018)
    * Control logic 
* **Button**: 
    * Database with Layout manager and Seattle Neighborhoods file (neighborhoods.geojson)
    * Callback manager that reacts on Button
    * Data manager that queries data for neighborhood, time of day, and year
    * Chart manager that displays statistical charts (e.g., time series, histograms, etc.) for traffic flow trends
    * Control logic 

## Preliminary Plan
1. Create dashboard template, including HTML divs for map, chart, and interactive components
2. Create function to load and join datasets
3. Create functions to display neighborhood map and traffic flow map
4: Create functions to display statistical charts
4. Create callback functions for interactive components
5. Create function to filter dataset based on current state
