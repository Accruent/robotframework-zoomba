*** Settings ***
Documentation   Zoomba GUI Library Tests
Library         ../../src/Zoomba/GUILibrary.py

*** Variables ***
${browser}     chrome

*** Test Cases ***
Wait for Keywords Test
    [Teardown]      Close All Browsers
    Open Browser    https://github.com/    browser=${browser}
    Maximize Browser Window
    Set Selenium Speed    0.1s
    wait for and input text      //input[@name='q']      robotframework
    press keys                    //input[@name='q']      RETURN
    wait for and click element               //a[@href='/robotframework/robotframework']
    wait until page contains element         //div[@id='readme']

Element value should be equal and not equal Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=${browser}
    Maximize Browser Window
    element value should be equal       btnK    Google Search
    element value should not be equal   btnK    Not Google Search

Save Selenium Screenshot Test
    [Teardown]                      Close All Browsers
    Open Browser                    http://www.google.com    browser=${browser}
    Maximize Browser Window
    Save Selenium Screenshot

Truncate String Test
    ${reallyLongTestString}=    set variable    This is a long String, which should be truncated here, unless it's the original string.
    ${truncatedTestString}=     set variable    This is a long String, which should be truncated here
    ${actualTruncatedString}=   truncate string     ${reallyLongTestString}    ${53}
    should be equal             ${truncatedTestString}      ${actualTruncatedString}
    ${actualTruncatedString2}=  truncate string     ${reallyLongTestString}    ${150}
    should be equal             ${reallyLongTestString}      ${actualTruncatedString2}

Scroll To Bottom of Page Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=${browser}
    Maximize Browser Window
    wait for and input text      //input[@name='q']      robot framework
    press keys                    //input[@name='q']      RETURN
    wait until element is visible                   //div[@id='res']
    scroll to bottom of page
    ${position} =                Execute Javascript        return window.pageYOffset
    should be equal              "767"         "${position}"

Wait Until Window Opens Test
    [Teardown]                      Close All Browsers
    Open Browser                    https://www.seleniumeasy.com/test/window-popup-modal-demo.html    browser=${browser}
    Maximize Browser Window
    Click Element                   //a[contains(text(),'Follow On Twitter')]
    Wait Until Window Opens         Selenium Easy (@seleniumeasy) on Twitter     10

Wait For and Select Window Test
    [Teardown]                      Close All Browsers
    Open Browser                    https://www.seleniumeasy.com/test/window-popup-modal-demo.html    browser=${browser}
    Maximize Browser Window
    Click Element                   //a[contains(text(),'Follow On Twitter')]
    Wait For and Select Window      Selenium Easy (@seleniumeasy) on Twitter

Wait Until Element Contains Value
    [Teardown]                      Close All Browsers
    Open Browser                    http://www.google.com                                              browser=${browser}
    Maximize Browser Window
    Input Text                      //input[@name='q']                                                  abc123
    Wait For And Click Element      btnK
    Wait Until Element Contains Value  //input[@name='q']                                               abc123