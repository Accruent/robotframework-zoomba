Zoomba
===========
!https://badge.fury.io/py/robotframework-zoomba.svg!:https://badge.fury.io/py/robotframework-zoomba
!https://travis-ci.org/Accruent/zoomba.svg?branch=master!:https://travis-ci.org/Accruent/zoomba
!https://coveralls.io/repos/github/Accruent/zoomba/badge.svg?branch=master!:https://coveralls.io/github/Accruent/zoomba?branch=master

Introduction
-----------

Zoomba is a collection of libraries spanning UI, REST API, and SOAP API automation using [Robot Framework](https://github.com/robotframework/robotframework).
These libraries are extensions of existing libraries [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary), [Requests](https://github.com/bulkan/robotframework-requests),
and [SudsLibrary](https://github.com/aljcalandra/robotframework-sudslibrary).

Zoomba adds a significant amount of data validation support for REST and SOAP APIs, and extends functionality for typical GUI automation.

As a team beginning the journey of automation with Robot Framework - we found that there was some time spent ramping up our libraries and
Zoomba aims to make that process easier for new projects.

See the **Keyword Documentation** for the [API](docs/APILibraryDocumentation.html), [SOAP](docs/SOAPLibrarydocumentation.html),
or [GUI](docs/GUILibraryDocumentation.html) library for more specific information about the functionality.


Getting Started
-----------

The Zoomba library is easily installed using the [`setup.py`](setup.py) file in the home directory.
Simply run the following command to install Zoomba and it's dependencies:

```python
pip install robotframework-zoomba
```

If you decide to pull the repo locally to make contributions or just want to play around with the code
you can install Zoomba by running the following from the *root directory*:
```python
pip install .
```

Contributing
------------

To make contributions please refer to the [CONTRIBUTING](CONTRIBUTING.rst) guidelines.


Support
--------
General Robot Framework questions should be directed to the [community forum](https://groups.google.com/forum/#!forum/robotframework-users).

Contact the team at `robosquad@accruent.com` with specific requests or questions regarding the Zoomba libraries!