#!/usr/bin/env python3

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = """
1.5.1
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
      maintainer   = 'Alex Calandra, Michael Hintz, Keith Smoland, Matthew Giardina',
      maintainer_email= 'calandra.aj@gmail.com',
      license      = 'apache',
      keywords     = 'Robot Framework',
      platforms    = 'any',
      install_requires= [
          "robotframework==3.0.2",
          "robotframework-requests>=0.4.7",
          "robotframework-seleniumlibrary>=3.0.1",
          "robotframework-sudslibrary-aljcalandra",
          "requests>=2.18.4",
          "selenium>=3.8.1",
          "python-dateutil"
      ],
      classifiers  = CLASSIFIERS,
      package_dir  = {'' : 'src'},
      packages     = ['Zoomba']
      )
