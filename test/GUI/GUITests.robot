*** Settings ***
Documentation   Zoomba GUI Library Tests
Library         ../../src/Zoomba/GUILibrary.py

*** Variables ***
${browser}     chrome

*** Keywords ***
Test Case Setup
    [Arguments]    ${url}=https://github.com/      ${browser}=${browser}
    Open Browser   ${url}    browser=${browser}
    Maximize Browser Window
    Set Selenium Speed    0.2s

*** Test Cases ***
Wait for Keywords Test
    [Teardown]      Close All Browsers
    Test Case Setup
    wait for and input text      //input[@name='q']      robotframework
    press keys                    //input[@name='q']      RETURN
    wait for and click element               //a[@href='/robotframework/robotframework']
    wait until page contains element         //div[@id='readme']

Element value should be equal and not equal Test
    [Teardown]      Close All Browsers
    Test Case Setup    http://www.google.com
    element value should be equal       btnK    Google Search
    element value should not be equal   btnK    Not Google Search

Save Selenium Screenshot Test
    [Teardown]                      Close All Browsers
    Test Case Setup    http://www.google.com
    ${file1}=                       Save Selenium Screenshot
    ${file2}=                       Save Selenium Screenshot
    Should Not Be Equal             ${file1}  ${file2}
    Should Match Regexp             ${file1}                    .selenium-screenshot-\\d{10}.\\d{0,8}-\\d.png

Iframe keywords Test
    [Teardown]      Close All Browsers
    Test Case Setup    https://www.w3schools.com/html/html_iframe.asp
    Page should not contain element     //a[@href='default.asp'][@class='active']
    wait for and select frame   //iframe[@src='default.asp']
    wait until page contains element    //a[@href='default.asp'][@class='active']
    Unselect frame
    Page should not contain element     //a[@href='default.asp'][@class='active']

Mouse over Keywords Test
    [Teardown]      Close All Browsers
    Test Case Setup    https://jquery.com/
    wait for and mouse over                 //a[contains(text(),'Download')]
    wait for and mouse over and click       //a[contains(text(),'Browser Support')]
    wait until page contains                Current Active Support

Wait Until Javascript Completes Test
    [Teardown]      Close All Browsers
    Test Case Setup    https://jquery.com/
    wait until page contains element       //a[@title='jQuery']
    wait until javascript is complete
    title should be                        jQuery

Web Elements Text Test
    [Teardown]      Close All Browsers
    Test Case Setup    http://www.google.com
    wait for and input text      //input[@name='q']      robot framework
    press keys                    //input[@name='q']      RETURN
    wait until element is visible                   //div[@id='res']
    ${resultsLinksList}=        Get Webelements     //div[@id='res']
    ${linksTextList}=           Get Text From Web Elements List     ${resultsLinksList}
    should contain     ${linksTextList}[0]     Robot Framework

Web Elements Vertical Position Test
    [Teardown]      Close All Browsers
    Test Case Setup    http://www.google.com
    wait for and input text      //input[@name='q']      robot framework
    press keys                    //input[@name='q']      RETURN
    wait until element is visible                       //div[@id='res']
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
    should be equal     ${testDict1}    ${newDict1}
    ${badValuesDict}=     create dictionary from keys and values lists        ${keysList}    ${badValuesList}
    should be equal     ${testDict2}    ${badValuesDict}

Truncate String Test
    ${reallyLongTestString}=    set variable    This is a long String, which should be truncated here, unless it's the original string.
    ${truncatedTestString}=     set variable    This is a long String, which should be truncated here
    ${actualTruncatedString}=   truncate string     ${reallyLongTestString}    ${53}
    should be equal             ${truncatedTestString}      ${actualTruncatedString}
    ${actualTruncatedString2}=  truncate string     ${reallyLongTestString}    ${150}
    should be equal             ${reallyLongTestString}      ${actualTruncatedString2}

Scroll To Bottom of Page Test
    [Teardown]      Close All Browsers
    Test Case Setup    http://www.google.com
    wait for and input text      //input[@name='q']      robot framework
    press keys                    //input[@name='q']      RETURN
    wait until element is visible                   //div[@id='res']
    scroll to bottom of page
    ${position} =                Execute Javascript        return window.pageYOffset
    should be equal              "767"         "${position}"

Wait Until Window Opens Test
    [Teardown]                      Close All Browsers
    Test Case Setup    https://www.seleniumeasy.com/test/window-popup-modal-demo.html
    Click Element                   //a[contains(text(),'Follow On Twitter')]
    Wait Until Window Opens         Selenium Easy (@seleniumeasy) / Twitter     10

Wait For and Select Window Test
    [Teardown]                      Close All Browsers
    Test Case Setup    https://www.seleniumeasy.com/test/window-popup-modal-demo.html
    Click Element                   //a[contains(text(),'Follow On Twitter')]
    Wait For and Select Window      Selenium Easy (@seleniumeasy) / Twitter     10

Wait Until Element Contains Value
    [Teardown]                      Close All Browsers
    Test Case Setup    http://www.google.com
    Input Text                      //input[@name='q']                                                  abc123
    Wait Until Element Contains Value  //input[@name='q']                                               abc123
