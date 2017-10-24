#!/usr/bin/env python

import os
import pip
import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

VERSION = """
1.0.4
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
      license      = '',
      keywords     = 'bots',
      platforms    = 'any',
      install_requires=[
      ],
      classifiers  = CLASSIFIERS,
      zip_safe     = True,
      packages     = ['zoomba']
      )