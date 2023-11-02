*** Settings ***
Documentation   Zoomba GUI Library Tests
Library         ../../src/Zoomba/GUILibrary.py
Library         Collections
Suite Setup    Test Case Setup
Suite Teardown   Close All Browsers
Force Tags      Edge

*** Keywords ***
Test Case Setup
    Open Browser   browser=Edge
    Maximize Browser Window
    Set Selenium Speed    0.05s

*** Test Cases ***
Wait for Keywords Test
    Go To      https://github.com/
    Wait For Page to Load
    Wait For And Click Element    //qbsearch-input
    wait for and input text      //input[@id='query-builder-test']      robotframework
    press keys                    //input[@id='query-builder-test']      RETURN
    wait for and click element               //a[@href='/robotframework/robotframework']
    wait until page contains element         //div[@id='readme']

Wait for Keywords Test With Password
    Go To      https://github.com/
    Wait For Page to Load
    Wait For And Click Element    //qbsearch-input
    wait for and input text      //input[@id='query-builder-test']      robotframework
    press keys                    //input[@id='query-builder-test']      RETURN
    wait for and click element               //a[@href='/robotframework/robotframework']
    wait until page contains element         //div[@id='readme']

Element value should be equal and not equal Test
    Go To    http://www.google.com
    Wait For Page to Load
    element value should be equal       btnK    Google Search
    element value should not be equal   btnK    Not Google Search

Save Selenium Screenshot Test
    Go To    http://www.google.com
    ${file1}=                       Save Selenium Screenshot
    ${file2}=                       Save Selenium Screenshot
    Should Not Be Equal             ${file1}  ${file2}
    Should Match Regexp             ${file1}                    .selenium-screenshot-\\d{10}.\\d{0,8}-\\d.png

Iframe keywords Test
    Go To    https://seleniumbase.io/w3schools/iframes
    Wait For Page to Load
    Page should not contain      This page is displayed in an iframe
    wait for and select frame   //iframe[@id='iframeResult']
    Unselect frame
    Page should not contain      This page is displayed in an iframe

Nested Iframe keyword Test
    Go To    https://www.quackit.com/html/tags/html_iframe_tag.cfm
    Wait For Page to Load
    Select Nested Frame    //iframe[@name='result4']     //iframe[@src='/html/tags/html_iframe_tag_example.cfm']

Mouse over Keywords Test
    Go To    https://jquery.com/
    Wait For Page to Load
    wait for and mouse over                 //a[contains(text(),'Download')]
    wait for and mouse over and click       //a[contains(text(),'Browser Support')]
    wait until page contains                Current Active Support

Wait Until Javascript Completes Test
    Go To    https://jquery.com/
    Wait For Page to Load
    wait until page contains element       //a[@title='jQuery']
    wait until javascript is complete
    title should be                        jQuery

Web Elements Text Test
    Go To    http://www.google.com
    Wait For Page to Load
    wait for and input text      //textarea[1]      robot framework
    press keys                    //textarea[1]       RETURN
    wait until element is visible                   //div[@id='res']
    ${resultsLinksList}=        Get Webelements     //div[@id='res']
    ${linksTextList}=           Get Text From Web Elements List     ${resultsLinksList}
    should contain     ${linksTextList}[0]     Robot Framework

Web Elements Vertical Position Test
    Go To    http://www.google.com
    Wait For Page to Load
    wait for and input text      //textarea[1]       robot framework
    press keys                    //textarea[1]       RETURN
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
    Go To    http://www.google.com
    Wait For Page to Load
    wait for and input text      //textarea[1]       robot framework
    press keys                    //textarea[1]       RETURN
    wait until element is visible                   //div[@id='res']
    scroll to bottom of page
    ${position} =                Execute Javascript        return window.pageYOffset
    Should Be True               ${position} > 700

Wait Until Window Tests
    Go To    https://www.quackit.com/html/codes/html_popup_window_code.cfm
    Wait For Page to Load
    Wait For And Select Frame       //iframe[@name='result1']
    Click Element                   //a[contains(text(),'Open a popup window')]
    Wait Until Window Opens         Popup Example     10
    Wait For and Select Window      Popup Example     10

Wait Until Element Contains Value
    Go To    http://www.google.com
    Wait For Page to Load
    Wait For And Input Text                      //textarea[1]                                                  abc123
    Wait Until Element Contains Value    //textarea[1]                                               abc123

Get Element CSS Attribute Value
    Go To    https://www.w3schools.com/html/html_examples.asp
    Wait For Page to Load
    ${value}=     Get Element CSS Attribute Value      //div[@id='googleSearch']       display
    Should Be Equal     ${value}     block

Element CSS Attribute Value Should Be
    Go To    https://www.w3schools.com/html/html_examples.asp
    Wait For Page to Load
    Element CSS Attribute Value Should Be      //div[@id='googleSearch']       display       block

Get React List Items Test
    Go To         https://react-select.com/home
    Wait For Page to Load
    ${selectXpath}=             Set Variable        //*[@id="root"]/div/div[2]/div[2]/div/div/div[1]/div[2]
    ${expectedLabels}=          Create List         Ocean    Blue    Purple    Red    Orange    Yellow    Green    Forest    Slate    Silver
    Wait Until Page Contains Element                ${selectXpath}
    Scroll Element Into View                        ${selectXpath}
    ${actualLabels}=    Get React List Labels       ${selectXpath}
    Lists Should Be Equal       ${expectedLabels}   ${actualLabels}     ignore_order=True

Test Mouse Scroll
    Set Selenium Speed    1s
    Go To    https://www.bgc.bard.edu/research-forum/articles/292/test-zoom-function-on-object
    Wait For Page to Load
    Scroll Element Into View    //body/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]
    Mouse Scroll Over Element  //body/div[6]/div[1]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]  y=-100
    Mouse Scroll     y=200

Test Disabled Elements
    Go To        https://demos.jquerymobile.com/1.4.5/forms-disabled
    Wait For Page to Load
    ${list_selection}=        Get Selected List Label   //select[@id='select-native-5']
    List Selection Should Be  //select[@id='select-native-5']      ${list_selection}