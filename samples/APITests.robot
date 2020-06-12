*** Settings ***
Documentation   Zoomba API Library Tests
Library         Zoomba.APILibrary
Variables       APITestsData.py
Test Setup      Suppress Insecure Request Warnings

*** Variables ***
&{headers}=       Content-Type=application/json      charset=UTF-8
${endpoint}=      https://jsonplaceholder.typicode.com
${endpoint_2}=    https://reqres.in/api

*** Test Cases ***
Call Get Request Basic Test
    ${resp}=   Call Get Request     ${headers}     ${endpoint}     /todos/1
    Validate Response Contains Expected Response     ${resp.text}    ${get_basic_expected}

Call Get Request Basic With Error Test
    ${resp}=   Call Get Request     ${headers}     ${endpoint}     /todos/1
    Run Keyword And Expect Error    ${get_basic_validation_error}   Validate Response Contains Expected Response     ${resp.text}    ${get_basic_error_expected}

Call Post Request With Ignored Keys Test
    ${resp}=   Call Post Request     ${headers}     ${endpoint_2}     /users     ${post_data}
    ${ignored_keys}=   create list     id     createdAt
    Validate Response Contains Expected Response     ${resp.text}    ${post_expected}   ignored_keys=${ignored_keys}

Call Put Request Test With Ignored Keys Test
    ${resp}=   Call Put Request     ${headers}     ${endpoint_2}     /users/2     ${put_data}
    ${ignored_keys}=   create list     id     updatedAt
    Validate Response Contains Expected Response     ${resp.text}    ${put_expected}    ignored_keys=${ignored_keys}

Call Patch Request Test With Ignored Keys Test
    ${resp}=   Call Patch Request     ${headers}     ${endpoint_2}     /users/2     ${put_data}
    ${ignored_keys}=   create list     id     updatedAt
    Validate Response Contains Expected Response     ${resp.text}    ${put_expected}    ignored_keys=${ignored_keys}

Call Delete Request Test With Ignored Keys Test
    ${resp}=   Call Delete Request     ${headers}     ${endpoint_2}     /users/2     ${put_data}
    Should Be True     ${resp.status_code} == 204

Validate Response Contains Expected Response Test
    Validate Response Contains Expected Response      ${key_by_key_actual}        ${key_by_key_expected}

Validate Response Contains Expected Response Error Test
    Run Keyword And Expect Error    ${key_by_key_error}     Validate Response Contains Expected Response      ${key_by_key_actual}        ${key_by_key_expected_error}
