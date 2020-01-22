*** Settings ***
Documentation   Zoomba Mobile Library Tests. Requires Appium Server running on port 4723 with an Android device/emulator available.
Library         ../../src/Zoomba/MobileLibrary.py
Test Setup      Start App
Test Teardown   Quit Application
Force Tags        Mobile

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  ${CURDIR}\\demo_app.apk

*** Keywords ***
Start App
    Open Application        ${REMOTE_URL}     platformName=Android    deviceName=Android   app=${APP}
    Wait For And Click Element       com.touchboarder.android.api.demos:id/buttonDefaultPositive
    Wait Until Page Contains      API Demos

*** Test Cases ***
Wait For And Click Element By Accessibility Id Keyword Test
    Wait For And Click Element       accessibility_id=More options
    Wait Until Page Contains      Change Log

Wait For And Click Element By Xpath Keyword Test
    Wait For And Click Element       //hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.ListView/android.widget.TextView[2]
    Wait Until Page Contains      Animation

Wait For And Input Text Keyword Test
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag and drop
    Wait Until Page Contains       Views/Drag and Drop

Wait For And Long Press Keyword Test
    Wait For And Long Press       accessibility_id=More options
    Wait Until Page Contains      Change Log

Wait For And Input Password Keyword Test
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Password        com.touchboarder.android.api.demos:id/search_src_text       drag and drop
    Wait Until Page Contains       Views/Drag and Drop

Wait Until Element is Enabled Keyword Test
    Wait Until Element Is Enabled       accessibility_id=More options

Drag and Drop Keyword Test
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    wait for and click text       Graphics/Shadow Card Drag
    Drag and Drop                 com.touchboarder.android.api.demos:id/card      com.touchboarder.android.api.demos:id/shape_select

Drag and Drop By Offset Keyword Test
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    wait for and click text       Graphics/Shadow Card Drag
    Drag and Drop By Offset                com.touchboarder.android.api.demos:id/card           200      200






