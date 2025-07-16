#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-fullstory',
      version='1.0.5',
      description='Singer.io tap for extracting data from the FullStory API',
      author='Stitch',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_fullstory'],
      install_requires=[
          'singer-python==1.9.1',
          'requests==2.32.4',
          'backoff==1.8.0',
          'pendulum==1.2.0',
          'ijson==2.3'
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
