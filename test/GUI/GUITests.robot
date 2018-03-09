*** Settings ***
Documentation   Zoomba GUI Library Tests
Library         ../../src/Zoomba/GUILibrary.py

*** Test Cases ***
Wait for Keywords Test
    [Teardown]      Close All Browsers
    Open Browser    https://github.com/    browser=chrome
    Maximize Browser Window
    wait for and input text      //input[@name='q']      robotframework
    press key                    //input[@name='q']      \\13
    wait for and click element               //a[@href='/robotframework/robotframework']
    wait until page contains element         //div[@id='readme']

Element value should be equal and not equal Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    element value should be equal       btnK    Google Search
    element value should not be equal   btnK    Not Google Search

Iframe keywords Test
    [Teardown]      Close All Browsers
    Open Browser    https://www.w3schools.com/html/html_iframe.asp    browser=chrome
    Maximize Browser Window
    Page should not contain element     //a[@href='default.asp'][@class='active']
    wait for and select frame   //iframe[@src='default.asp']
    wait until page contains element    //a[@href='default.asp'][@class='active']
    Unselect frame
    Page should not contain element     //a[@href='default.asp'][@class='active']

Mouse over Keywords Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.amazon.com    browser=chrome
    Maximize Browser Window
    wait for and mouse over                 //span[@class='nav-line-2' and contains(.,'Departments')]
    wait for and mouse over                 //span[@class='nav-text' and .='Amazon Music']
    wait for and mouse over and click       //span[@class='nav-text' and .='Prime Music']
    wait until page contains element        //title[.='Amazon.com: Prime Music']

Wait Until Javascript Completes Test
    [Teardown]      Close All Browsers
    Open Browser    https://jquery.com/    browser=chrome
    Maximize Browser Window
    wait until page contains element       //a[@title='jQuery']
    wait until javascript is complete
    title should be                        jQuery

Web Elements Text Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and input text      lst-ib      robot framework
    press key                    lst-ib      \\13
    wait until element is visible                   //h3[@class='r']//a
    ${resultsLinksList}=        Get Webelements     //h3[@class='r']//a
    ${linksTextList}=           Get Text From Web Elements List     ${resultsLinksList}
    should be equal     @{linksTextList}[0]     Robot Framework

Web Elements Vertical Position Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and input text      lst-ib      robot framework
    press key                    lst-ib      \\13
    wait until element is visible                       //h3[@class='r']//a
    ${resultsLinksList}=            Get Webelements     //h3[@class='r']//a
    ${linksPositionList}=           Get Vertical Position From Web Elements List        ${resultsLinksList}
    should be equal                 @{linksPositionList}[0]     ${175}

Create Dictionary from Lists Test
    ${testDict1}=       create dictionary   Name=User1      ID=01   Phone=51212345678
    ${keysList}=        create list     Name    ID      Phone
    ${valuesList}=      create list     User1   01      51212345678
    ${badValuesList}=   create list     User1   02      51254515212     More Stuff
    ${newDict1}=        create dictionary from keys and values lists        ${keysList}    ${valuesList}
    should be equal     ${testDict1}    ${newDict1}
    ${badValuesStatus}=     run keyword and return status       create dictionary from keys and values lists        ${keysList}    ${badValuesList}
    should not be true      ${badValuesStatus}
    run keyword and expect error    *ValueError: The length of the keys and values lists is not the same: \nKeys Length: 3\nValues Length: 4
    ...                             create dictionary from keys and values lists        ${keysList}    ${badValuesList}

Truncate String Test
    ${reallyLongTestString}=    set variable    This is a long String, which should be truncated here, unless it's the original string.
    ${truncatedTestString}=     set variable    This is a long String, which should be truncated here
    ${actualTruncatedString}=   truncate string     ${reallyLongTestString}    ${53}
    should be equal             ${truncatedTestString}      ${actualTruncatedString}
    ${actualTruncatedString2}=  truncate string     ${reallyLongTestString}    ${150}
    should be equal             ${reallyLongTestString}      ${actualTruncatedString2}

Drag and Drop by JS Test
    [Teardown]      Close All Browsers
    Open Browser                        https://html5demos.com/drag/    browser=chrome
    Drag and Drop by JS                 //a[@id='one']      //div[@id='bin']
    Page Should Not Contain Element     //a[@id='one']

Scroll To Bottom of Page Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and input text      lst-ib      robot framework
    press key                    lst-ib      \\13
    wait until element is visible                   //h3[@class='r']//a
    scroll to bottom of page
    ${position} =                Execute Javascript        return window.pageYOffset
    should be equal              "878"         "${position}"