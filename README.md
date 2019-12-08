<!--- README template from https://github.com/scottydocs/README-template.md -->

# Neighborhood Traffic Flow

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
[![GitHub contributors](https://img.shields.io/github/contributors/Neighborhood-Traffic-Flow/neighborhood-traffic-flow)](#contributors)
[![GitHub license](https://img.shields.io/github/license/Neighborhood-Traffic-Flow/neighborhood-traffic-flow)](./LICENSE)
[![Build Status](https://travis-ci.org/Neighborhood-Traffic-Flow/neighborhoodtrafficflow.svg?branch=master)](https://travis-ci.org/Neighborhood-Traffic-Flow/neighborhoodtrafficflow)
[![Coverage Status](https://coveralls.io/repos/github/Neighborhood-Traffic-Flow/neighborhoodtrafficflow/badge.svg?branch=master)](https://coveralls.io/github/Neighborhood-Traffic-Flow/neighborhoodtrafficflow?branch=master)


An interactive dashboard to explore traffic flow trends in Seattle neighborhoods.

Final Project for [CSE 583: Software Engineering for Data Scientists](https://uwseds.github.io/)

## Installation and Use

#### To clone the repository:
```
git clone https://github.com/Neighborhood-Traffic-Flow/neighborhoodtrafficflow.git
cd neighborhoodtrafficflow
```

#### To set up the `conda` environment:
```
conda env create -f environment.yml
conda activate ntf
pip install -e .
```
Note: The above is a one-time step.

#### To run the dashboard:
Start the server, then open a web browser with the following URL: http://127.0.0.1:8050/
```
conda activate ntf
cd neighborhoodtrafficflow
python app.py
```
Note: The `conda activate` step only needs to be done once per shell instance.

## Contributors

Thanks to the following people who have contributed to this project:

* [@agesak](https://github.com/agesak)
* [@kels271828](https://github.com/kels271828)
* [@resquenazi](https://github.com/resquenazi)
* [@siqicheng88](https://github.com/siqicheng88)


## License

This project is [MIT](./LICENSE) licenced.
