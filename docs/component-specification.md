# Component Specification

<!---
The document should have sections for:
* **Software components** High level description of the software components such as: *data manager*, which provides a simplified interface to your data and provides application specific features (e.g., querying data subsets); and *visualization manager*, which displays data frames as a plot. Describe at least 3 components specifying what it does, inputs it requires, and outputs it provides.
* **Interactions to accomplish use cases** Describe how the above software components interact to accomplish at least one of your use cases.
* **Preliminary plan** A list of tasks in priority order.
--->

## Software Components

![](flowchart.png)

* **Data manager**: Pre-process raw data
   * What it does: Load raw data, join data by neighborhood and street, reformat data for Plotly figures
   * Input: Data from Zillow and City of Seattle
   * Output: Reformatted csv files and Pandas DataFrames to dashboard and figure managers
* **Dashboard manager**: HTML structure of dashboard
   * What it does: Create HTML components for headers, maps, charts, and interactive components
   * Input: Data from data manager, current state of interactive components from browser, Plotly figures from figure manager
   * Output: Current state of interactive components to figure manager, HTML components to browser
* **Figure manager**: Create Plotly figures
   * What it does: Create Plotly figures for maps and charts
   * Input: Data from data manager, current state of interactive components from dashboard manager
   * Ouput: Plotly figures to dashboard manager

## Preliminary Plan
1. Initialize package structure in repository, including CI and tests
2. Create functions to pre-process raw data
3. Create dashboard template, including HTML components for maps, charts, and interactive components
4. Create CSS stylesheet to make dashboard look nice
5. Create functions to create Plotly maps and charts
6. Create callback functions to update Plotly maps and charts
