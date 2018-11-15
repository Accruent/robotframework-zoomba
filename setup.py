#!/usr/bin/env python3

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = """
1.6.1
""".strip()

DESCRIPTION = """
Zoomba
""".strip()

CLASSIFIERS  = """
Development Status :: 5 - Production/Stable
Operating System :: OS Independent
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework :: Library
""".strip().splitlines()

setup(name         = 'robotframework-zoomba',
      version      = VERSION,
      description  = 'Robot Framework mini-framework.',
      long_description = DESCRIPTION,
      url          = 'https://github.com/Accruent/zoomba',
      maintainer   = 'Alex Calandra, Michael Hintz, Keith Smoland, Matthew Giardina, Brandon Wolfe',
      maintainer_email= 'robosquad@accruent.com',
      license      = 'apache',
      keywords     = 'Robot Framework',
      platforms    = 'any',
      install_requires= [
          "robotframework>=3.0.4",
          "robotframework-requests>=0.5.0",
          "robotframework-seleniumlibrary>=3.2.0",
          "robotframework-sudslibrary-aljcalandra",
          "requests>=2.20.1",
          "selenium>=3.141.0",
          "python-dateutil"
      ],
      classifiers  = CLASSIFIERS,
      package_dir  = {'' : 'src'},
      packages     = ['Zoomba']
      )
