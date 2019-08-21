Zoomba
===========
!https://badge.fury.io/py/robotframework-zoomba.svg!:https://badge.fury.io/py/robotframework-zoomba
!https://travis-ci.org/Accruent/robotframework-zoomba.svg?branch=master!:https://travis-ci.org/Accruent/robotframework-zoomba
!https://coveralls.io/repos/github/Accruent/robotframework-zoomba/badge.svg?branch=master!:https://coveralls.io/github/Accruent/robotframework-zoomba?branch=master

Introduction
-----------

Zoomba is a collection of libraries spanning UI, REST API, and SOAP API automation using [Robot Framework](https://github.com/robotframework/robotframework).
These libraries are extensions of existing libraries [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary), [Requests](https://github.com/bulkan/robotframework-requests),
[SudsLibrary](https://github.com/aljcalandra/robotframework-sudslibrary), and [AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary).

Zoomba adds a significant amount of data validation support for REST and SOAP APIs, extends functionality for typical Web GUI automation, and
extends AppiumLibrary functionality to support Windows desktop automation.

As a team beginning the journey of automation with Robot Framework - we found that there was some time spent ramping up our libraries and
Zoomba aims to make that process easier for new projects.

See the **Keyword Documentation** for the [API](https://accruent.github.io/robotframework-zoomba/docs/APILibraryDocumentation.html), [SOAP](https://accruent.github.io/robotframework-zoomba/docs/SOAPLibrarydocumentation.html),
[GUI](https://accruent.github.io/robotframework-zoomba/docs/GUILibraryDocumentation.html), or [Desktop](https://accruent.github.io/robotframework-zoomba/docs/DesktopLibrarydocumentation.html) library for more specific information about the functionality.


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

If you plan to run Windows desktop automation you will need to have a running appium server. To do so first have [Node](https://nodejs.org/en/download/)
installed and then run the following:
```python
npm install -g appium
appium
```
Alternatively [Appium Desktop](https://github.com/appium/appium-desktop/releases) can be used.

Additionally if you run the following command new documentation will be generated on each commit :
```python
git config core.hooksPath .githooks
```

Examples
-----------
Example tests can be found in the [test directory](test).

Contributing
------------

To make contributions please refer to the [CONTRIBUTING](CONTRIBUTING.rst) guidelines.


Support
--------
General Robot Framework questions should be directed to the [community forum](https://groups.google.com/forum/#!forum/robotframework-users).

Contact the team at `robosquad@accruent.com` with specific requests or questions regarding the Zoomba libraries!