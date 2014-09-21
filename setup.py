
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My project',
    'author': 'gers',
    'url': 'wherever',
    'download_url': 'wherever',
    'author_email': 'gers',
    'version:': '0.1',
    'install_requires': ['nose'],
    'packages': ['shopping_scraper'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
