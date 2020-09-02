Zoomba
===========
[![PyPI version](https://badge.fury.io/py/robotframework-zoomba.svg)](https://badge.fury.io/py/robotframework-zoomba)
[![Build Status](https://travis-ci.com/Accruent/robotframework-zoomba.svg?branch=master)](https://travis-ci.org/Accruent/robotframework-zoomba)
[![Coverage Status](https://coveralls.io/repos/github/Accruent/robotframework-zoomba/badge.svg?branch=master)](https://coveralls.io/github/Accruent/robotframework-zoomba?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/accruent/robotframework-zoomba/badge)](https://www.codefactor.io/repository/github/accruent/robotframework-zoomba)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Accruent/robotframework-zoomba.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Accruent/robotframework-zoomba/alerts/)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAccruent%2Frobotframework-zoomba.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FAccruent%2Frobotframework-zoomba?ref=badge_shield)

Introduction
--------------

Zoomba is a collection of libraries spanning GUI, REST API, SOAP API, Mobile, and Windows Desktop automation using [Robot Framework](https://github.com/robotframework/robotframework).
These libraries are extensions of existing libraries [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary), [Requests](https://github.com/bulkan/robotframework-requests), 
[SudsLibrary](https://github.com/aljcalandra/robotframework-sudslibrary), and [AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary).

Zoomba adds a significant amount of data validation support for REST and SOAP APIs, extends functionality for typical Web GUI automation, and
extends AppiumLibrary functionality to support Windows desktop automation.

As a team beginning the journey of automation with Robot Framework - we found that there was some time spent ramping up our libraries and Zoomba aims to make that process easier for new projects.

See the **Keyword Documentation** for the [API](https://accruent.github.io/robotframework-zoomba/APILibraryDocumentation.html), [SOAP](https://accruent.github.io/robotframework-zoomba/SOAPLibraryDocumentation.html),
[GUI](https://accruent.github.io/robotframework-zoomba/GUILibraryDocumentation.html), [Mobile](https://accruent.github.io/robotframework-zoomba/MobileLibraryDocumentation.html), or [Desktop](https://accruent.github.io/robotframework-zoomba/DesktopLibraryDocumentation.html) library for more specific information about the functionality.

Example tests can be found in the [samples directory](https://github.com/Accruent/robotframework-zoomba/tree/master/samples).

Some Features of the Library
--------------
#### [GUI Library](https://accruent.github.io/robotframework-zoomba/GUILibraryDocumentation.html):
When working with web pages of varying load times you probably find yourself running a lot of calls like so:
```robotframework
Wait Until Page Contains Element      locator
Click Element                         locator
```
For ease of use we have combined a lot of these into simple one line keywords:
```robotframework
Wait For And Click Element      locator
Wait For And Click Text         text
Wait For And Select From List   list_locator    target_locator
```
Another keyword that is particularly useful is for when you are waiting for javascript to complete on a page before proceeding:
```robotframework
Wait For And Click Element       locator that leads to a new page with javascript     
Wait Until Javascript Is Complete
Wait For And Click Element       locator
```

#### [API Library](https://accruent.github.io/robotframework-zoomba/APILibraryDocumentation.html):
This library wraps the [requests library](https://github.com/bulkan/robotframework-requests) so we have created a set of keywords to easily allow users to make requests in a single keyword:
```robotframework
Call Get Request       ${headers_dictionary}    endpoint    query_string
Call Post Request      ${headers_dictionary}    endpoint    query_string     ${data_payload}
```

After receiving your data we made it incredibly easy to validate it. [Validate Response Contains Expected Response](https://accruent.github.io/robotframework-zoomba/APILibraryDocumentation.html#Validate%20Response%20Contains%20Expected%20Response) takes your received request and compares it to your expected data. If there are any errors found it will report line by line what they are.
```robotframework
Validate Response Contains Expected Response    ${json_actual_response}      ${json_expected_response}
```
If there is any mismatched data it will look something like this:
```
Key(s) Did Not Match:
------------------
Key: pear
Expected: fish
Actual: bird
------------------
Full List Breakdown:
Expected: [{'apple': 'cat', 'banana': 'dog', 'pear': 'fish'}, {'apple': 'cat', 'banana': 'mice', 'pear': 'bird'}, {'apple': 'dog', 'banana': 'mice', 'pear': 'cat'}]
Actual: [{'apple': 'cat', 'banana': 'dog', 'pear': 'bird'}]

Please see differing value(s)
```
If you wanted to ignore a key such as the 'update_date' you would simply set the 'ignored_keys' variable to that key or a list of keys:
```robotframework
Validate Response Contains Expected Response    ${json_actual_response}      ${json_expected_response}      ignored_keys=update_date
Validate Response Contains Expected Response    ${json_actual_response}      ${json_expected_response}      ignored_keys=${list_of_keys}
```

#### [Mobile Library](https://accruent.github.io/robotframework-zoomba/MobileLibraryDocumentation.html):
Extending the [AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary) we again add some quality of life 'Wait For And' type keywords:
```robotframework
Wait For And Click Element      locator
Wait For And Click Text         text
Wait Until Element Contains     locator     text
```
There are of course additional features that have yet to be implemented in AppiumLibrary:
```robotframework
Drag and Drop      source_locator     target_locator
Drag And Drop By Offset     locator    x_offset     y_offset
Scroll Down To Text       text
Scroll Up To Text         text
```

#### [Desktop Library](https://accruent.github.io/robotframework-zoomba/DesktopLibraryDocumentation.html):
Also extends [AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary) to tailor it Windows desktop automation. This includes enhancements to base keywords such as [Open Application](https://accruent.github.io/robotframework-zoomba/DesktopLibraryDocumentation.html#Open%20Application) or [Click Element](https://accruent.github.io/robotframework-zoomba/DesktopLibraryDocumentation.html#Click%20Element) to perform better for windows. Other notable additions include:

Start and Stop the WinAppDriver as needed (best used for suite setup/teardown:
```robotframework
Driver Setup
Driver Teardown
```
Easily switching to new windows or the desktop session:
```robotframework
Switch Application      Desktop
Switch Application By Name     remote_url    new_window_name
```
A variety of keywords for controlling the mouse:
```robotframework
Mouse Over Element     locator
Mouse Over and Click Element    locator
Mouse over and Context Click Element    locator
Mouse Over By Offset     x_offset    y_offset
```
Keywords for dragging and dropping:
```robotframework
Drag and Drop      source_locator     target_locator
Drag And Drop By Offset     locator    x_offset     y_offset
```
The ability to send key commands to the application:
```robotframework
Send Keys     \\ue00      p     \\ue00
Send Keys To Element    locator     a     b     c
```
Selecting an element from a combobox:
```robotframework
Select Element From ComboBox     combobox_locator      element_locator
```

Getting Started
----------------

The Zoomba library is easily installed using the [`setup.py`](https://github.com/Accruent/robotframework-zoomba/blob/master/setup.py) file in the home directory.
Simply run the following command to install Zoomba and it's dependencies:

```python
pip install robotframework-zoomba
```

If you decide to pull the repo locally to make contributions or just want to play around with the code
you can install Zoomba by running the following from the *root directory*:
```python
pip install .
```

To access the keywords in the library simply add the following to your robot file settings (depending on what you need):
```python
*** Settings ***
Library    Zoomba.APILibrary
Library    Zoomba.GUILibrary
Library    Zoomba.SOAPLibrary
Library    Zoomba.MobileLibrary
Library    Zoomba.DesktopLibrary
```

Additional Setup Information
---------------------------------

If you plan to run Mobile automation you will need to have a running appium server. To do so first have [Node](https://nodejs.org/en/download/)
installed and then run the following:
```python
npm install -g appium
appium
```
Alternatively [Appium Desktop](https://github.com/appium/appium-desktop/releases) can be used.

For Windows automation we suggest [installing and using the WinAppDriver](https://github.com/Microsoft/WinAppDriver/releases) without Appium as it seems to be much more stable.

Examples
------------
Example tests can be found in the [samples directory](https://github.com/Accruent/robotframework-zoomba/tree/master/samples).

The [test directory](https://github.com/Accruent/robotframework-zoomba/tree/master/test) may also contain tests but be aware that these are used for testing releases and may not be as straight forward to use as the ones in the [samples directory](https://github.com/Accruent/robotframework-zoomba/tree/master/samples).


Contributing
-----------------

To make contributions please refer to the [CONTRIBUTING](https://github.com/Accruent/robotframework-zoomba/blob/master/CONTRIBUTING.rst) guidelines.

Additionally if you run the following command new documentation will be generated on each commit :
```python
git config core.hooksPath .githooks
```

Support
---------------
General Robot Framework questions should be directed to the [community forum](https://forum.robotframework.org/).

Contact the team at `robosquad@accruent.com` or create an issue with specific requests or questions regarding the Zoomba libraries!
