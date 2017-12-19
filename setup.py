#!/usr/bin/env python3

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from distutils.core import setup

VERSION = """
1.1.0
""".strip()

DESCRIPTION = """
Zoomba
""".strip()

CLASSIFIERS  = """
Development Status :: 5 - Production/Stable
Operating System :: OS Independent
Programming Language :: Python 3
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
          "robotframework==3.0.2",
          "robotframework-requests==0.4.7",
          "robotframework-selenium2library==3.0.0",
          "robotframework-extendedselenium2library==0.9.1",
          "robotframework-debuglibrary==1.0.2",
          "robotframework-databaselibrary==1.0.1",
          "requests==2.18.4",
          "selenium==3.8.0"
      ],
      classifiers  = CLASSIFIERS,
      zip_safe     = True,
      package_dir  = {'' : 'src'},
      packages     = ['Zoomba']
      )