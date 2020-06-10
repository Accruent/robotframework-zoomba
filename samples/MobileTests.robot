*** Settings ***
Documentation    Zoomba Mobile Library Tests. Requires Appium Server running on port 4723 with an Android device/emulator available.
Library          Zoomba.MobileLibrary
Suite Setup      Start App
Test Setup       Reset App
Suite Teardown   Close Application
Force Tags       Mobile

*** Variables ***
${REMOTE_URL}           http://localhost:4723/wd/hub
${APP}                  ${CURDIR}${/}..\\test\\Helpers\\demo_app.apk
${commandTimeout}=      120

*** Keywords ***
Start App
    Open Application        ${REMOTE_URL}     platformName=Android    automationName=UiAutomator2    deviceName=Android
    ...                     newCommandTimeout=${commandTimeout}       app=${APP}

Reset App
    Reset Application
    Wait For And Click Element       com.touchboarder.android.api.demos:id/buttonDefaultPositive
    Wait Until Page Contains         API Demos

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
    Wait For And Long Press       //hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.ListView/android.widget.TextView[2]
    Wait Until Page Contains      Animation

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

Drag and Drop Keyword Test Failure
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    wait for and click text       Graphics/Shadow Card Drag
    Run keyword And Expect Error         ValueError: Element locator 'Not_a_real_id' did not match any elements.
    ...            Drag and Drop         Not_a_real_id      com.touchboarder.android.api.demos:id/shape_select

Drag and Drop By Offset Keyword Test
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    wait for and click text       Graphics/Shadow Card Drag
    Drag and Drop By Offset                com.touchboarder.android.api.demos:id/card           200      200

Wait Until Element Contains
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    Wait Until Element Contains    //hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.ListView/android.widget.TextView[1]
    ...                            Views/Drag and Drop

Wait Until Element Does Not Contain
    Wait For And Click Element       accessibility_id=Search
    Wait For And Input Text        com.touchboarder.android.api.demos:id/search_src_text       drag
    Wait Until Element Does Not Contain    //hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.ListView/android.widget.TextView[1]
    ...                            Some Other Text

Scroll To Text Keyword Test
    Wait For And Click Text     API Demos
    Wait For And Click Text     Graphics
    Scroll Down To Text    SensorTest
    Scroll Up To Text      Arcs

Wait For And Tap Keyword Test
    Wait For And Tap      accessibility_id=Search
    Wait Until Page Contains    com.touchboarder.android.api.demos:id/search_src_text

Save Selenium Screenshot Test
    ${file1}=                       Save Appium Screenshot
    ${file2}=                       Save Appium Screenshot
    Should Not Be Equal             ${file1}  ${file2}
    Should Match Regexp             ${file1}                    appium-screenshot-\\d{8,10}.\\d{6,8}-\\d.png






