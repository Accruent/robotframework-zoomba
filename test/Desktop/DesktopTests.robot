*** Settings ***
Documentation   Zoomba Desktop Library Tests. Requires Appium Server running on port 4723.
Library         ../../src/Zoomba/DesktopLibrary.py
Test Setup      Start App
Test Teardown   Quit Application

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  Microsoft.WindowsCalculator_8wekyb3d8bbwe!App

*** Keywords ***
Start App
    Open Application        ${REMOTE_URL}     platformName=Windows    deviceName=Windows   app=${APP}
    Maximize Window

*** Test Cases ***
Wait For And Click Element By Id Keyword Test
    Wait For And Click Element       accessibility_id=num2Button
    Wait Until Page Contains      2

Wait For And Click Element By Name Keyword Test
    Wait For And Click Element       name=Two
    Wait Until Page Contains      2

Wait For And Click Element By Class Keyword Test
    Wait For And Click Element       class=Button

Wait For And Input Text By Id Keyword Test
    Wait For And Input Text        accessibility_id=CalculatorResults       12345
    Wait Until Page Contains       12,345

Wait For And Input Text By Name Keyword Test
    Wait For And Input Text        name=Display is 0       12345
    Wait Until Page Contains       12,345

Wait For And Input Text By Id Keyword Test
    Wait For And Long Press       accessibility_id=num2Button
    Wait Until Page Contains      2


