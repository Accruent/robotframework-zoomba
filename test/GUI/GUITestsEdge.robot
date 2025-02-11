*** Settings ***
Documentation               Zoomba GUI Library Tests
Library                     ../../src/Zoomba/GUILibrary.py
Library                     Collections
Suite Setup                 Test Case Setup
Suite Teardown              Close All Browsers
Test Tags                   Edge


*** Variables ***
${DUCKDUCK_SEARCH_URL}    https://duckduckgo.com
${DUCKDUCK_SEARCH}        //input[@id='searchbox_input']
${RF_PAGE_TEXT}        Robot Framework is an open source automation framework for test automation
${RF_LINK}              //a[@href='https://robotframework.org/']
${ALT_URL1}             http://www.google.com
${TEXT_AREA}            //textarea[1]
${CHECK_DIV}            //section[@data-testid='mainline']


*** Test Cases ***
Wait For Keywords Test
    Go To                   ${DUCKDUCK_SEARCH_URL}
    Wait Until Javascript Is Complete
    Wait For And Input Text                             ${DUCKDUCK_SEARCH}            robotframework
    Press Keys              ${DUCKDUCK_SEARCH}          RETURN
    Wait For And Click Element                          ${RF_LINK}
    Wait Until Page Contains                            ${RF_PAGE_TEXT}

Wait For Keywords Test With Password
    Go To                   ${DUCKDUCK_SEARCH_URL}
    Wait Until Javascript Is Complete
    Wait For And Input Text                             ${DUCKDUCK_SEARCH}            robotframework
    Press Keys              ${DUCKDUCK_SEARCH}          RETURN
    Wait For And Click Element                          ${RF_LINK}
    Wait Until Page Contains                            ${RF_PAGE_TEXT}

Element Value Should Be Equal And Not Equal Test
    Go To                   ${ALT_URL1}
    Wait For Page To Load
    Element Value Should Be Equal                       btnK                        Google Search
    Element Value Should Not Be Equal                   btnK                        Not Google Search

Save Selenium Screenshot Test
    Go To                   ${ALT_URL1}
    ${file1}                Save Selenium Screenshot
    ${file2}                Save Selenium Screenshot
    Should Not Be Equal     ${file1}                    ${file2}
    Should Match Regexp     ${file1}                    .selenium-screenshot-\\d{10}.\\d{0,8}-\\d.png

Iframe Keywords Test
    Go To                   https://seleniumbase.io/w3schools/iframes
    Wait For Page To Load
    Page Should Not Contain                             This page is displayed in an iframe
    Wait For And Select Frame                           //iframe[@id='iframeResult']
    Unselect Frame
    Page Should Not Contain                             This page is displayed in an iframe

Nested Iframe Keyword Test
    [Tags]                  robot:skip      # The nested iframe here is no loner working
    Go To                   https://www.quackit.com/html/tags/html_iframe_tag.cfm
    Wait For Page To Load
    Select Nested Frame     //iframe[@name='result4']   //iframe[@src='/html/tags/html_iframe_tag_example.cfm']

Mouse Over Keywords Test
    Go To                   https://jquery.com/
    Wait For Page To Load
    Wait For And Mouse Over                             //a[contains(text(),'Download')]
    Wait For And Mouse Over And Click                   //a[contains(text(),'Browser Support')]
    Wait Until Page Contains                            Current Active Support

Wait Until Javascript Completes Test
    Go To                   https://jquery.com/
    Wait For Page To Load
    Wait Until Page Contains Element                    //a[@title='jQuery']
    Wait Until Javascript Is Complete
    Title Should Be         jQuery

Web Elements Text Test
    Go To                   ${DUCKDUCK_SEARCH_URL}
    Wait For Page To Load
    Wait For And Input Text                             ${DUCKDUCK_SEARCH}                robot framework
    Press Keys              ${DUCKDUCK_SEARCH}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    ${resultsLinksList}     Get Webelements             ${CHECK_DIV}
    ${linksTextList}        Get Text From Web Elements List                         ${resultsLinksList}
    Should Contain          ${linksTextList}[0]         Robot Framework

Web Elements Vertical Position Test
    Go To                   ${DUCKDUCK_SEARCH_URL}
    Wait For Page To Load
    Wait For And Input Text                             ${DUCKDUCK_SEARCH}                robot framework
    Press Keys              ${DUCKDUCK_SEARCH}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    ${resultsLinksList}     Get Webelements             ${CHECK_DIV}
    ${linksPositionList}    Get Vertical Position From Web Elements List            ${resultsLinksList}
    Should Be True          ${linksPositionList}[0] > ${140}

Create Dictionary From Lists Test
    ${testDict1}  Create Dictionary  Name=User1  ID=01  Phone=51212345678
    ${testDict2}  Create Dictionary  Name=User1  ID=02  Phone=51254515212
    ${keysList}             Create List                 Name                        ID                          Phone
    ${valuesList}  Create List  User1  01  51212345678
    ${badValuesList}  Create List  User1  02  51254515212  More Stuff
    ${newDict1}  Create Dictionary From Keys And Values Lists  ${keysList}  ${valuesList}
    Should Be Equal         ${testDict1}                ${newDict1}
    ${badValuesDict}  Create Dictionary From Keys And Values Lists  ${keysList}  ${badValuesList}
    Should Be Equal         ${testDict2}                ${badValuesDict}

Truncate String Test
    ${reallyLongTestString}                             Set Variable
    ...                     This is a long String, which should be truncated here, unless it's the original string.
    ${truncatedTestString}  Set Variable                This is a long String, which should be truncated here
    ${actualTruncatedString}                            Truncate String             ${reallyLongTestString}     ${53}
    Should Be Equal         ${truncatedTestString}      ${actualTruncatedString}
    ${actualTruncatedString2}                           Truncate String             ${reallyLongTestString}     ${150}
    Should Be Equal         ${reallyLongTestString}     ${actualTruncatedString2}

Scroll To Bottom Of Page Test
    Go To                   ${DUCKDUCK_SEARCH_URL}
    Wait For Page To Load
    Wait For And Input Text                             ${DUCKDUCK_SEARCH}                robot framework
    Press Keys              ${DUCKDUCK_SEARCH}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    Scroll To Bottom Of Page
    ${position}             Execute Javascript          return window.pageYOffset
    Should Be True          ${position} > 700

Wait Until Element Contains Value
    Go To                   ${ALT_URL1}
    Wait For Page To Load
    Wait For And Input Text                             ${TEXT_AREA}                abc123
    Wait Until Element Contains Value                   ${TEXT_AREA}                abc123

Get Element CSS Attribute Value
    Go To                   https://www.w3schools.com/html/html_examples.asp
    Wait For Page To Load
    ${value}                Get Element CSS Attribute Value                         //div[@id='googleSearch']   display
    Should Be Equal         ${value}                    block

Element CSS Attribute Value Should Be
    Go To                   https://www.w3schools.com/html/html_examples.asp
    Wait For Page To Load
    Element CSS Attribute Value Should Be               //div[@id='googleSearch']   display                     block

Get React List Items Test
    Go To                   https://react-select.com/home
    Wait For Page To Load
    ${selectXpath}          Set Variable                //*[@id="root"]/div/div[2]/div[2]/div/div/div[1]/div[2]
    ${expectedLabels}  Create List  Ocean  Blue  Purple  Red  Orange  Yellow  Green  Forest  Slate  Silver
    Wait Until Page Contains Element                    ${selectXpath}
    Scroll Element Into View                            ${selectXpath}
    ${actualLabels}         Get React List Labels       ${selectXpath}
    Lists Should Be Equal   ${expectedLabels}           ${actualLabels}             ignore_order=True

Test Mouse Scroll
    [Tags]                  robot:skip      # The site is no longer available
    Set Selenium Speed      1s
    Go To                   https://www.bgc.bard.edu/research-forum/articles/292/test-zoom-function-on-object
    Wait For Page To Load
    Set Test Variable  ${MOUSE_SCROLL_CHECK}  //body/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]
    Scroll Element Into View                            ${MOUSE_SCROLL_CHECK}
    Mouse Scroll Over Element                           ${MOUSE_SCROLL_CHECK}       y=-100
    Mouse Scroll            y=200

Test Disabled Elements
    Go To                   https://demos.jquerymobile.com/1.4.5/forms-disabled
    Wait For Page To Load
    ${list_selection}       Get Selected List Label     //select[@id='select-native-5']
    List Selection Should Be  //select[@id='select-native-5']  ${list_selection}

Wait Until Window Tests
    [Tags]                  robot:skip      # The site is no longer available
    Go To                   https://www.quackit.com/html/html_editors/scratchpad/preview.cfm?example=/html/codes/html_popup_window_code
    Wait For Page To Load
    Wait For And Click Element           //a[contains(text(),'Open a popup window')]
    Wait Until Window Opens                             Popup Example               10
    Wait For And Select Window                          Popup Example               10

Select From Search Field Test
    Go To                                https://jquery.com/
    Wait For Page To Load
    Select From Search Field             //input[@type='search']     css()
    Wait Until Javascript Is Complete
    Page Should Contain                  css()

*** Keywords ***
Test Case Setup
    Open Browser            browser=Edge
    Maximize Browser Window
    Set Selenium Speed      0.08s
