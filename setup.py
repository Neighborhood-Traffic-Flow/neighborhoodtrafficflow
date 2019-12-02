"""Initialize the project after it has been cloned."""
from setuptools import setup, find_packages

PACKAGES = find_packages()

opts = dict(
    name='neighborhoodtrafficflow',
    description='An interactive dashboard to explore traffic flow trends ' \
        'in Seattle neighborhoods.',
    url='https://github.com/Neighborhood-Traffic-Flow/' \
        'neighborhood-traffic-flow',
    license='MIT',
    author='Neighborhood-Traffic-Flow',
    version='1.0',
    packages=PACKAGES
)


if __name__ == '__main__':
    setup(**opts)