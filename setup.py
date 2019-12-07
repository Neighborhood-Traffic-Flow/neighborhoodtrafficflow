"""Initialize the project after it has been cloned."""
from setuptools import setup, find_packages

PACKAGES = find_packages()
DESCRIPTION = 'An interactive dashboard to explore traffic flow trends in ' \
    'Seattle neighborhoods.'
URL = 'https://github.com/Neighborhood-Traffic-Flow/neighborhood-traffic-flow'

OPTS = dict(
    name='neighborhoodtrafficflow',
    description=DESCRIPTION,
    url=URL,
    license='MIT',
    author='Neighborhood-Traffic-Flow',
    version='1.0',
    packages=PACKAGES
)


if __name__ == '__main__':
    setup(**OPTS)
