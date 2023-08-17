RobotFramework-Zoomba
===========
[![PyPI version](https://badge.fury.io/py/robotframework-zoomba.svg)](https://badge.fury.io/py/robotframework-zoomba)
[![Downloads](https://static.pepy.tech/badge/robotframework-zoomba)](https://pepy.tech/project/robotframework-zoomba)
[![Build Status](https://github.com/Accruent/robotframework-zoomba/workflows/tests/badge.svg?branch=master)](https://github.com/Accruent/robotframework-zoomba/actions?query=workflow%3Atests)
[![Coverage Status](https://coveralls.io/repos/github/Accruent/robotframework-zoomba/badge.svg?branch=master)](https://coveralls.io/github/Accruent/robotframework-zoomba?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/accruent/robotframework-zoomba/badge)](https://www.codefactor.io/repository/github/accruent/robotframework-zoomba)

What is RobotFramework-Zoomba?
--------------

Robotframework-Zoomba is a collection of libraries spanning GUI, REST API, and SOAP API automation using [Robot Framework](https://github.com/robotframework/robotframework).
These libraries are extensions of existing libraries [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary), [Requests](https://github.com/bulkan/robotframework-requests), 
and [SudsLibrary](https://github.com/aljcalandra/robotframework-sudslibrary).

### Looking for our extension of [AppiumLibrary](https://github.com/serhatbolsu/robotframework-appiumlibrary) (DesktopLibrary and MobileLibrary)? Check out our new repo [RobotFramework-ApplicationLibrary](https://github.com/Accruent/robotframework-applicationlibrary)!

Zoomba adds a significant amount of data validation support for REST and SOAP API and extends functionality for typical Web GUI automation.

As a team beginning the journey of automation with Robot Framework - we found that there was some time spent ramping up our libraries and Robotframework-Zoomba aims to make that process easier for new projects.

See the **Keyword Documentation** for the [API](https://accruent.github.io/robotframework-zoomba/APILibraryDocumentation.html), [SOAP](https://accruent.github.io/robotframework-zoomba/SOAPLibraryDocumentation.html),
or [GUI](https://accruent.github.io/robotframework-zoomba/GUILibraryDocumentation.html) library for more specific information about the functionality.

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

or if you intend to run unit tests:
```python
pip install .[testing]
```

To access the keywords in the library simply add the following to your robot file settings (depending on what you need):
```python
*** Settings ***
Library    Zoomba.APILibrary
Library    Zoomba.GUILibrary
Library    Zoomba.SOAPLibrary
```

Examples
------------
Example tests can be found in the [samples directory](https://github.com/Accruent/robotframework-zoomba/tree/master/samples).

The [test directory](https://github.com/Accruent/robotframework-zoomba/tree/master/test) may also contain tests but be aware that these are used for testing releases and may not be as straight forward to use as the ones in the [samples directory](https://github.com/Accruent/robotframework-zoomba/tree/master/samples).


Contributing
-----------------

To make contributions please refer to the [CONTRIBUTING](https://github.com/Accruent/robotframework-zoomba/blob/master/CONTRIBUTING.rst) guidelines.

See the [.githooks](https://github.com/Accruent/robotframework-zoomba/tree/master/.githooks) directory for scripts to help in development. 

Support
---------------
General Robot Framework questions should be directed to the [community forum](https://forum.robotframework.org/).

For questions and issues specific to Zoomba please create an [issue](https://github.com/Accruent/robotframework-zoomba/issues) here on Github.
