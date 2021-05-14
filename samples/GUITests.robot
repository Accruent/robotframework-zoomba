*** Settings ***
Documentation   Zoomba GUI Library Tests
Library         Zoomba.GUILibrary    #plugins=Zoomba.Helpers.EdgePlugin    #Enable if using Edge

*** Variables ***
${browser}     chrome

*** Keywords ***
Test Case Setup
    [Arguments]    ${url}=https://github.com/      ${browser}=${browser}
    Open Browser   ${url}    browser=${browser}
    #Enable if using Edge:
    #Open Browser   ${url}    browser=${browser}     options=use_chromium=True
    Maximize Browser Window
    Set Selenium Speed    0.2s

*** Test Cases ***
Wait for Keywords Test
    [Setup]         Test Case Setup
    [Teardown]      Close All Browsers
    Wait For And Input Text      //input[@name='q']      robotframework
    Press Keys                    //input[@name='q']      RETURN
    Wait For And Click Element               //a[@href='/robotframework/robotframework']
    Wait Until Page Contains Element         //div[@id='readme']

Wait for Keywords Test With Password
    [Setup]         Test Case Setup
    [Teardown]      Close All Browsers
    Wait For And Input Password      //input[@name='q']      robotframework
    Press Keys                    //input[@name='q']      RETURN
    Wait For And Click Element               //a[@href='/robotframework/robotframework']
    Wait Until Page Contains Element         //div[@id='readme']

Element Value Should Be Equal and not equal Test
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]      Close All Browsers
    Element Value Should Be Equal       btnK    Google Search
    Element Value Should Not Be Equal   btnK    Not Google Search

Save Selenium Screenshot Test
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]                      Close All Browsers
    ${file1}=                       Save Selenium Screenshot
    ${file2}=                       Save Selenium Screenshot
    Should Not Be Equal             ${file1}  ${file2}
    Should Match Regexp             ${file1}                    .selenium-screenshot-\\d{10}.\\d{0,8}-\\d.png

Iframe keywords Test
    [Setup]         Test Case Setup        https://www.w3schools.com/html/html_iframe.asp
    [Teardown]      Close All Browsers
    Page Should Not Contain Element     //a[@href='default.asp'][@class='active']
    Wait For And Select Frame   //iframe[@src='default.asp']
    Wait Until Page Contains Element    //a[@href='default.asp'][@class='active']
    Unselect Frame
    Page Should Not Contain Element     //a[@href='default.asp'][@class='active']

Nested Iframe keyword Test
    [Teardown]      Close All Browsers
    Test Case Setup    https://www.quackit.com/html/tags/html_iframe_tag.cfm
    Select Nested Frame    //iframe[@name='result4']     //iframe[@src='/html/tags/html_iframe_tag_example.cfm']

Mouse over Keywords Test
    [Setup]         Test Case Setup        https://jquery.com/
    [Teardown]      Close All Browsers
    Wait For And Mouse Over                 //a[contains(text(),'Download')]
    Wait For And Mouse Over And Click       //a[contains(text(),'Browser Support')]
    Wait Until Page Contains                Current Active Support

Wait Until Javascript Completes Test
    [Setup]         Test Case Setup        https://jquery.com/
    [Teardown]      Close All Browsers
    Test Case Setup    https://jquery.com/
    Wait Until Page Contains Element       //a[@title='jQuery']
    Wait Until Javascript Is Complete
    Title Should Be                        jQuery

Web Elements Text Test
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]      Close All Browsers
    Wait For And Input Text      //input[@name='q']      robot framework
    Press Keys                    //input[@name='q']      RETURN
    Wait Until Element Is Visible                   //div[@id='res']
    ${resultsLinksList}=        Get Webelements     //div[@id='res']
    ${linksTextList}=           Get Text From Web Elements List     ${resultsLinksList}
    Should Contain     ${linksTextList}[0]     Robot Framework

Web Elements Vertical Position Test
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]      Close All Browsers
    Wait For And Input Text      //input[@name='q']      robot framework
    Press Keys                    //input[@name='q']      RETURN
    Wait Until Element Is Visible                       //div[@id='res']
    ${resultsLinksList}=            Get Webelements     //div[@id='res']
    ${linksPositionList}=           Get Vertical Position From Web Elements List        ${resultsLinksList}
    Should Be True                 ${linksPositionList}[0] > ${170}

Create Dictionary from Lists Test
    ${testDict1}=       create dictionary   Name=User1      ID=01   Phone=51212345678
    ${testDict2}=       create dictionary   Name=User1      ID=02   Phone=51254515212
    ${keysList}=        create list     Name    ID      Phone
    ${valuesList}=      create list     User1   01      51212345678
    ${badValuesList}=   create list     User1   02      51254515212     More Stuff
    ${newDict1}=        create dictionary from keys and values lists        ${keysList}    ${valuesList}
    Should Be Equal     ${testDict1}    ${newDict1}
    ${badValuesDict}=     create dictionary from keys and values lists        ${keysList}    ${badValuesList}
    Should Be Equal     ${testDict2}    ${badValuesDict}

Truncate String Test
    ${reallyLongTestString}=    set variable    This is a long String, which should be truncated here, unless it's the original string.
    ${truncatedTestString}=     set variable    This is a long String, which should be truncated here
    ${actualTruncatedString}=   truncate string     ${reallyLongTestString}    ${53}
    Should Be Equal             ${truncatedTestString}      ${actualTruncatedString}
    ${actualTruncatedString2}=  truncate string     ${reallyLongTestString}    ${150}
    Should Be Equal             ${reallyLongTestString}      ${actualTruncatedString2}

Scroll To Bottom of Page Test
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]      Close All Browsers
    Wait For And Input Text      //input[@name='q']      robot framework
    Press Keys                    //input[@name='q']      RETURN
    Wait Until Element Is Visible                   //div[@id='res']
    scroll to bottom of page

Wait Until Window Tests
    [Teardown]                      Close All Browsers
    Test Case Setup    https://www.quackit.com/html/codes/html_popup_window_code.cfm
    Wait For And Select Frame       //iframe[@name='result1']
    Click Element                   //a[contains(text(),'Open a popup window')]
    Wait Until Window Opens         Popup Example     10
    Wait For and Select Window      Popup Example     10

Wait Until Element Contains Value
    [Setup]         Test Case Setup        http://www.google.com
    [Teardown]                      Close All Browsers
    Input Text                      //input[@name='q']                                                  abc123
    Wait Until Element Contains Value  //input[@name='q']                                               abc123

Get Element CSS Attribute Value
    [Teardown]                      Close All Browsers
    Test Case Setup    https://www.w3schools.com/html/html_examples.asp
    ${value}=     Get Element CSS Attribute Value      //div[@id='googleSearch']       position
    Should Be Equal     ${value}     absolute

Element CSS Attribute Value Should Be
    [Teardown]                      Close All Browsers
    Test Case Setup    https://www.w3schools.com/html/html_examples.asp
    Element CSS Attribute Value Should Be      //div[@id='googleSearch']       position       absolute
