*** Settings ***
Documentation   Zoomba Desktop Library Tests. Requires Appium Server running on port 4723.
Library         ../../src/Zoomba/DesktopLibrary.py

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  Microsoft.WindowsCalculator_8wekyb3d8bbwe!App


*** Test Cases ***
Open / Maximize / Quit Application Keyword Test
    [Teardown]      Quit Application
    Open Application        ${REMOTE_URL}     platformName=Windows    deviceName=Windows   app=${APP}
    Maximize Window
