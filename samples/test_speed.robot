*** Settings ***
Documentation     Zoomba Desktop Library Tests.
Library           Zoomba.DesktopLibrary
#Suite Setup       Start App
#Test Setup        Start App
Test Teardown     Quit Application
#Suite Teardown    Driver Teardown
Force Tags        Windows

*** Variables ***
${REMOTE_URL}           http://127.0.0.1:4723
${APP}                  Microsoft.WindowsCalculator_8wekyb3d8bbwe!App


*** Test Cases ***
Switch To Desktop Test
    Open Application    ${REMOTE_URL}     platformName=Windows    deviceName=Windows   app=Root
#    log source
#    Wait For And Click Element           name=Start
#    Wait FOr And Input Text              xapth=Button[@ClassName=\"Button\"][@Name=\"Type here to search\"]"
#    Wait For And Click Element           xpath=//Button[@ClassName="Start"][@Name="Start"]
#    Wait For And Click Element           xpath=//Button[@ClassName="Start"][@Name="Start"]
     Wait For And Mouse Over Element      xpath=//Button[@ClassName="Start"][@Name="Start"]
