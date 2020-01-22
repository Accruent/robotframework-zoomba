*** Settings ***
Documentation   Zoomba Mobile Library Tests. Requires Appium Server running on port 4723 with an Android device/emulator available.
Library         ../../src/Zoomba/MobileLibrary.py
Test Setup      Start App
Test Teardown   Quit Application
Force Tags        Mobile

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  ${CURDIR}\\selendroid-test-app.apk

*** Keywords ***
Start App
    Open Application        ${REMOTE_URL}     platformName=Android    deviceName=Android   app=${APP}

*** Test Cases ***
Wait For And Click Element By Id Keyword Test
    Wait For And Click Element       io.selendroid.testapp:id/showToastButton
    Wait Until Page Contains      Hello selendroid toast!

Wait For And Click Element By accessibilityID Keyword Test
    Wait For And Click Element       accessibility_Id=startUserRegistrationCD
    Wait Until Page Contains      Username

Wait For And Click Element By Xpath Keyword Test
    Wait For And Click Element       //android.widget.ImageButton[@content-desc="startUserRegistrationCD"]
    Wait Until Page Contains      Username

Wait For And Input Text Keyword Test
    Wait For And Input Text        io.selendroid.testapp:id/my_text_field       12345
    Wait Until Page Contains       12345

Wait For And Long Press Keyword Test
    Wait For And Long Press       io.selendroid.testapp:id/waitingButtonTest
    Wait Until Page Contains      Waiting Dialog

Wait For And Input Password Keyword Test
    Wait For And Click Element       accessibility_Id=startUserRegistrationCD
    Wait For And Input Password        io.selendroid.testapp:id/inputPassword       12345

Wait Until Element is Enabled Keyword Test
    Wait Until Element Is Enabled       io.selendroid.testapp:id/showToastButton


