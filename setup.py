#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-closeio',
      version='0.6.2',
      description='Singer.io tap for extracting data from the CloseIO API',
      author='Stitch',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_closeio'],
      install_requires=[
          'singer-python==1.6.0a2',
          'requests==2.12.4',
          'backoff==1.3.2'
      ],
      entry_points='''
          [console_scripts]
          tap-closeio=tap_closeio:main
      ''',
      packages=['tap_closeio'],
      package_data = {
          'tap_closeio/schemas': [
              'leads.json',
              'activities.json'
          ]
      },
      include_package_data=True,
)
