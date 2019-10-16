#!/usr/bin/env python3

import version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='robotframework-zoomba',
      version=version.VERSION,
      description='Robot Framework mini-framework.',
      long_description='Zoomba',
      url='https://github.com/Accruent/zoomba',
      maintainer='Alex Calandra, Michael Hintz, Keith Smoland, Matthew Giardina, Brandon Wolfe',
      maintainer_email='robosquad@accruent.com',
      license='apache',
      keywords='Robot Framework robot-framework selenium requests appium soap',
      platforms='any',
      install_requires=requirements,
      extras_require={
        'testing': [
          'Appium-Python-Client'
        ]
      },
      classifiers="""
        Development Status :: 5 - Production/Stable
        Operating System :: OS Independent
        Programming Language :: Python :: 3
        Topic :: Software Development :: Testing
        Framework :: Robot Framework :: Library
        """.strip().splitlines(),
      package_dir={'': 'src'},
      packages=['Zoomba']
      )
