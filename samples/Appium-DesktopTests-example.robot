*** Settings ***
Documentation     Zoomba Desktop Library Tests.
Library           Zoomba.DesktopLibrary
Suite Setup       Start App
Suite Teardown    Close All Applications
Force Tags        Windows

*** Variables ***
${REMOTE_URL}           http://127.0.0.1:4723/wd/hub
${APP}                  Microsoft.WindowsCalculator_8wekyb3d8bbwe!App

*** Keywords ***
Start App
    [Documentation]     Sets up the application for quick launching through 'Launch Application'
    Open Application    ${REMOTE_URL}     platformName=Windows    deviceName=Windows   app=${APP}
    Maximize Window

*** Test Cases ***
Mouse Over Element Keyword Test
    Mouse Over Element     name=Two
    Mouse Over And Click Element     name=Two
    Mouse Over And Click Element     name=Two     x_offset=400   y_offset=100
    Mouse Over And Context Click Element     name=Two
    Mouse Over And Click Element     name=Two    double_click=True
    Mouse Over By Offset    100    -200
    Click A Point
