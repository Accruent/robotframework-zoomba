*** Settings ***
Documentation   Zoomba Desktop Library Tests. Requires Appium Server running on port 4723.
Library         ../../src/Zoomba/DesktopLibrary.py
#Suite Setup     Start App
#Test Setup      Launch Application
#Test Teardown   Quit Application
#Suite Teardown    Close All Applications
Force Tags        Windows

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  Microsoft.WindowsCalculator_8wekyb3d8bbwe!App

*** Test Cases ***
Select Element From Combobox Test
    switch application by name        ${REMOTE_URL}     window_name=Snipping Tool    platformName=Windows    deviceName=Windows   app=${APP}
    click text      Options
    Select Element From Combobox      accessibility_id=1019         name=Aqua     True
#    Select Element From Combobox      accessibility_id=Units1         name=Knots    False
#    Select Element From Combobox      accessibility_id=TogglePaneButton         accessibility_id=Standard

