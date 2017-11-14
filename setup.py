#!/usr/bin/env python

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

VERSION = """
1.0.1
""".strip()

DESCRIPTION = """
Zoomba
""".strip()

CLASSIFIERS  = """
Development Status :: 5 - Production/Stable
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Communication
""".strip().splitlines()

setup(name         = 'zoomba',
      version      = VERSION,
      description  = 'Robot Framework mini-framework.',
      long_description = DESCRIPTION,
      url          = 'https://github.com/Accruent/zoomba',
      license      = 'apache',
      keywords     = 'Robot Framework',
      platforms    = 'any',
      install_requires= [
          "robotframework==3.0",
          "robotframework-requests==0.4.5",
          "robotframework-selenium2library==1.7.4",
          "robotframework-extendedselenium2library==0.9.1",
          "robotframework-debuglibrary==0.8",
          "robotframework-databaselibrary==0.8.1",
          "robotframework-sudslibrary==0.8",
          "requests==2.11.1",
          "selenium==2.53.6"
      ],
      classifiers  = CLASSIFIERS,
      zip_safe     = True,
      package_dir  = {'' : 'src'},
      packages     = ['Zoomba']
      )