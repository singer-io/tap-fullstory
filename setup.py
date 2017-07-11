#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-fullstory',
      version='0.1.1',
      description='Singer.io tap for extracting data from the FullStory API',
      author='Stitch',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_fullstory'],
      install_requires=[
          'singer-python==1.6.0',
          'requests==2.12.4',
          'backoff==1.3.2',
          'pendulum==1.2.0'
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
