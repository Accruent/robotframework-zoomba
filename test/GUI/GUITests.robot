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
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and mouse over                 //div[@class='FPdoLc VlcLAe']//input[@name='btnK']
    wait for and mouse over                 //a[contains(text(),'Gmail')]
    wait for and mouse over and click       //a[contains(text(),'About')]
    wait until page contains element        //a[contains(text(),'About')]

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
    wait for and input text      //input[@name='q']      robot framework
    press key                    //input[@name='q']      \\13
    wait until element is visible                   //div[@id='res']
    ${resultsLinksList}=        Get Webelements     //div[@id='res']
    ${linksTextList}=           Get Text From Web Elements List     ${resultsLinksList}
    should contain     @{linksTextList}[0]     Robot Framework

Web Elements Vertical Position Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and input text      //input[@name='q']      robot framework
    press key                    //input[@name='q']      \\13
    wait until element is visible                       //div[@id='res']
    ${resultsLinksList}=            Get Webelements     //div[@id='res']
    ${linksPositionList}=           Get Vertical Position From Web Elements List        ${resultsLinksList}
    should be equal                 @{linksPositionList}[0]     ${172}

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

Drag and Drop by JS Test
    [Tags]          Broken
    [Teardown]      Close All Browsers
    Open Browser                        https://html5demos.com/drag/    browser=chrome
    Maximize Browser Window
    Drag and Drop by JS                 //a[@id='one']      //div[@id='bin']
    Page Should Not Contain Element     //a[@id='one']

Scroll To Bottom of Page Test
    [Teardown]      Close All Browsers
    Open Browser    http://www.google.com    browser=chrome
    Maximize Browser Window
    wait for and input text      //input[@name='q']      robot framework
    press key                    //input[@name='q']      \\13
    wait until element is visible                   //div[@id='res']
    scroll to bottom of page
    ${position} =                Execute Javascript        return window.pageYOffset
    should be equal              "767"         "${position}"