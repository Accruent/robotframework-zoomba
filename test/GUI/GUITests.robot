*** Settings ***
Documentation               Zoomba GUI Library Tests
Library                     ../../src/Zoomba/GUILibrary.py
Library                     Collections
Test Teardown               Close All Browsers


*** Variables ***
${browser}              chrome
${GITHUB_SEARCH}        //input[@id='query-builder-test']
${GITHUB_README}        //span[contains(text(),'README')]
${RF_LINK}              //a[@href='/robotframework/robotframework']
${ALT_URL1}             http://www.google.com
${TEXT_AREA}            //textarea[1]
${CHECK_DIV}            //div[@id='res']


*** Test Cases ***
Wait For Keywords Test
    Test Case Setup
    Press Keys              ${None}                     /
    Wait For And Input Text                             ${GITHUB_SEARCH}            robotframework
    Press Keys              ${GITHUB_SEARCH}            RETURN
    Wait For And Click Element                          ${RF_LINK}
    Wait Until Page Contains Element                    ${GITHUB_README}

Wait For Keywords Test With Password
    Test Case Setup
    Press Keys              ${None}                     /
    Wait For And Input Password                         ${GITHUB_SEARCH}            robotframework
    Press Keys              ${GITHUB_SEARCH}            RETURN
    Wait For And Click Element                          ${RF_LINK}
    Wait Until Page Contains Element                    ${GITHUB_README}

Element Value Should Be Equal And Not Equal Test
    Test Case Setup         ${ALT_URL1}
    Element Value Should Be Equal                       btnK                        Google Search
    Element Value Should Not Be Equal                   btnK                        Not Google Search

Save Selenium Screenshot Test
    Test Case Setup         ${ALT_URL1}
    ${file1}                Save Selenium Screenshot
    ${file2}                Save Selenium Screenshot
    Should Not Be Equal     ${file1}                    ${file2}
    Should Match Regexp     ${file1}                    .selenium-screenshot-\\d{10}.\\d{0,8}-\\d.png

Iframe Keywords Test
    Set Test Variable       ${CHECK_ELEMENT}            //a[@href='default.asp'][@class='active']
    Test Case Setup         https://www.w3schools.com/html/html_iframe.asp
    Page Should Not Contain Element                     ${CHECK_ELEMENT}
    Wait For And Select Frame                           //iframe[@src='default.asp']
    Wait Until Page Contains Element                    ${CHECK_ELEMENT}
    Unselect Frame
    Page Should Not Contain Element                     ${CHECK_ELEMENT}

Nested Iframe Keyword Test
    Test Case Setup         https://www.quackit.com/html/tags/html_iframe_tag.cfm
    Select Nested Frame     //iframe[@name='result4']   //iframe[@src='/html/tags/html_iframe_tag_example.cfm']

Mouse Over Keywords Test
    Test Case Setup         https://jquery.com/
    Wait For And Mouse Over                             //a[contains(text(),'Download')]
    Wait For And Mouse Over And Click                   //a[contains(text(),'Browser Support')]
    Wait Until Page Contains                            Current Active Support

Wait Until Javascript Completes Test
    Test Case Setup         https://jquery.com/
    Wait Until Page Contains Element                    //a[@title='jQuery']
    Wait Until Javascript Is Complete
    Title Should Be         jQuery

Web Elements Text Test
    Test Case Setup         ${ALT_URL1}
    Wait For And Input Text                             ${TEXT_AREA}                robot framework
    Press Keys              ${TEXT_AREA}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    ${resultsLinksList}     Get Webelements             ${CHECK_DIV}
    ${linksTextList}        Get Text From Web Elements List                         ${resultsLinksList}
    Should Contain          ${linksTextList}[0]         Robot Framework

Web Elements Vertical Position Test
    Test Case Setup         ${ALT_URL1}
    Wait For And Input Text                             ${TEXT_AREA}                robot framework
    Press Keys              ${TEXT_AREA}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    ${resultsLinksList}     Get Webelements             ${CHECK_DIV}
    ${linksPositionList}    Get Vertical Position From Web Elements List            ${resultsLinksList}
    Should Be True          ${linksPositionList}[0] > ${160}

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
    Test Case Setup         ${ALT_URL1}
    Wait For And Input Text                             ${TEXT_AREA}                robot framework
    Press Keys              ${TEXT_AREA}                RETURN
    Wait Until Element Is Visible                       ${CHECK_DIV}
    Scroll To Bottom Of Page
    ${position}             Execute Javascript          return window.pageYOffset
    Should Be True          ${position} > 700

Wait Until Window Tests
    Test Case Setup         https://www.quackit.com/html/codes/html_popup_window_code.cfm
    Wait For And Select Frame                           //iframe[@name='result1']
    Wait For And Click Element           //a[contains(text(),'Open a popup window')]
    Wait Until Window Opens                             Popup Example               10
    Wait For And Select Window                          Popup Example               10

Wait Until Element Contains Value
    Test Case Setup         ${ALT_URL1}
    Input Text              ${TEXT_AREA}                abc123
    Wait Until Element Contains Value                   ${TEXT_AREA}                abc123

Get Element CSS Attribute Value
    Test Case Setup         https://www.w3schools.com/html/html_examples.asp
    ${value}                Get Element CSS Attribute Value                         //div[@id='googleSearch']   display
    Should Be Equal         ${value}                    block

Element CSS Attribute Value Should Be
    Test Case Setup         https://www.w3schools.com/html/html_examples.asp
    Element CSS Attribute Value Should Be               //div[@id='googleSearch']   display                     block

Get React List Items Test
    [Setup]                 Test Case Setup             https://react-select.com/home
    ${selectXpath}          Set Variable                //*[@id="root"]/div/div[2]/div[2]/div/div/div[1]/div[2]
    ${expectedLabels}  Create List  Ocean  Blue  Purple  Red  Orange  Yellow  Green  Forest  Slate  Silver
    Wait Until Page Contains Element                    ${selectXpath}
    Scroll Element Into View                            ${selectXpath}
    ${actualLabels}         Get React List Labels       ${selectXpath}
    Lists Should Be Equal   ${expectedLabels}           ${actualLabels}             ignore_order=True

Test Mouse Scroll
    [Setup]                 Test Case Setup             https://www.bgc.bard.edu/research-forum/articles/292/test-zoom-function-on-object
    Set Test Variable  ${MOUSE_SCROLL_CHECK}  //body/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]
    Set Selenium Speed      1s
    Scroll Element Into View                            ${MOUSE_SCROLL_CHECK}
    Mouse Scroll Over Element                           ${MOUSE_SCROLL_CHECK}       y=-100
    Mouse Scroll            y=200

Test Disabled Elements
    [Setup]                 Test Case Setup             https://demos.jquerymobile.com/1.4.5/forms-disabled
    Set Test Variable       ${LIST_CHECK}               //select[@id='select-native-5']
    ${list_selection}       Get Selected List Label     ${LIST_CHECK}
    List Selection Should Be                            ${LIST_CHECK}               ${list_selection}


*** Keywords ***
Test Case Setup
    [Arguments]             ${url}=https://github.com/  ${browser}=${browser}
    Open Browser            ${url}                      browser=${browser}
    Maximize Browser Window
    Wait For Page To Load
    Set Selenium Speed      0.06s
