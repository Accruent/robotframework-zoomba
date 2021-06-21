*** Settings ***
Documentation     Zoomba GUI/Desktop Library Tests using a WebView ap[plication
Library           Zoomba.DesktopLibrary
Library           Zoomba.GUILibrary   plugins=Zoomba.Helpers.EdgePlugin
Suite Setup       Driver Setup
test Teardown     Zoomba.DesktopLibrary.close all applications
Suite Teardown    Driver Teardown
Force Tags        Windows

*** Variables ***
${REMOTE_URL}           http://127.0.0.1:4723
# This app link will be the location of your compiled WebView application, using this demo app here:
# https://docs.microsoft.com/en-us/microsoft-edge/webview2/how-to/webdriver
${WebView_APP}          C:/Git/WebView2Samples/SampleApps/WebView2APISample/Debug/Win32/WebView2APISample.exe

*** Test Cases ***
Test WebView App
    # Open your WebView App, url optional (GUILibrary Keyword)
    Open WebView Application   ${WebView_APP}     https://www.github.com
    # Click an element in the web page (GUILibrary Keyword)
    Zoomba.GUILibrary.Wait For And Click Element    //header/div[1]/div[2]/nav[1]/ul[1]/li[2]/a[1]
    # Connect to your WebView application's app frame (DesktopLibrary Keyword)
    Switch Application By Locator    ${REMOTE_URL}   class=WEBVIEW2APISAMPLE
    # Clicking a button outside the web view, in this case the 'Back' button (DesktopLibrary Keyword)
    Zoomba.DesktopLibrary.Wait For And Click Element    name=Back
    # Click an element in the web page, just to demonstate that we can still issue commands there as well
    Zoomba.GUILibrary.Wait For And Click Element    //header/div[1]/div[2]/nav[1]/ul[1]/li[2]/a[1]
