#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-fullstory',
      version='1.0.4',
      description='Singer.io tap for extracting data from the FullStory API',
      author='Stitch',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_fullstory'],
      install_requires=[
          'singer-python==6.1.1',
          'requests==2.31.0',
          'backoff>=2.2.1,<3',
          'pendulum==3.1.0',
          'ijson==3.4.0'
      ],
      entry_points='''
          [console_scripts]
          tap-fullstory=tap_fullstory:main
      ''',
      packages=['tap_fullstory'],
      package_data = {
          'tap_fullstory/schemas': [
              'events.json'
          ]
      },
      include_package_data=True,
)
