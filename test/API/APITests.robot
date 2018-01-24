*** Settings ***
Documentation   Zoomba API Library Tests
Library         ../../src/Zoomba/APILibrary.py
Library         Collections
Variables       ZoombaAPITestsData.py

*** Test Cases ***
Validate Response Positive Tests
    [Template]      Validate Response Contains Expected Response
#   JSON Actual         Expected Dict           Ignored Keys    Full List       Identity Key
# --- Common Case ------------------------------------------------------------------------------------------------------
    ${json_actual_1}    ${dict_expected_1}
# --- Common Case with Ignored key on wrong value ----------------------------------------------------------------------
    ${json_actual_1}    ${dict_expected_2}      pear
# --- Common Case with Ignored key on wrong value, margin_type doesn't affect results-----------------------------------
    ${json_actual_1}    ${dict_expected_2}      pear             margin_type=hours
# --- Common Case on identical Lists with Identity Key -----------------------------------------------------------------
    ${json_actual_2}    ${list_expected_1}      ${NONE}          ${FALSE}        apple
# --- Expected list with one item inside of the Actual using Identity Key that is not unique ---------------------------
    ${json_actual_4}    ${list_expected_1}      ${NONE}          ${FALSE}        apple
# --- Expected list with one item inside of the Actual using Identity Key that is unique -------------------------------
    ${json_actual_6}    ${list_expected_7}      ${NONE}          ${FALSE}        id
# --- Expected item list within Actual response using Identity Key and ignoring a non existent key ---------------------
    ${json_actual_6}    ${list_expected_7}      whatever         ${FALSE}        id
# --- Expected item within Actual response using Identity Key and ignoring a key with mismatched values ----------------
    ${json_actual_5}    ${list_expected_1}      pear             ${FALSE}        apple
# --- Identical Lists using Top Level Only flag with identity Key that exists on the items -----------------------------
    ${json_actual_3}    ${list_expected_4}      ${NONE}          ${TRUE}         apple
# --- Identical Lists using Top Level Only flag with identity Key doesn't exists on the items --------------------------
    ${json_actual_3}    ${list_expected_4}      ${NONE}          ${TRUE}         whatever
# --- Identical Lists using Top Level Only flag with no identity Key ---------------------------------------------------
    ${json_actual_3}    ${list_expected_4}      ${NONE}          ${TRUE}         ${NONE}


Validate Response Negative Tests
    [Template]      Validate Response Contains Expected Response Errors Template
#   Error               JSON Actual         Expected Dict           Ignored Keys    Full List       Identity Key     **kwargs
# --- Empty Actual Response dictionary----------------------------------------------------------------------------------
    ${empty_resp_err}   ${EMPTY}            ${dict_expected_1}
# --- Empty Actual Response dictionary----------------------------------------------------------------------------------
    ${empty_resp_err}   ${empty_list}       ${list_expected_1}
# --- No match on some keys on single dictionary -----------------------------------------------------------------------
    ${not_match1}       ${json_actual_1}    ${dict_expected_2}
# --- No match on some keys on single dictionary with ignored key ------------------------------------------------------
    ${not_match1}       ${json_actual_1}    ${dict_expected_2}      apple
# --- No match on some keys on single dictionary with ignored key, margin_type doesn't affect results-------------------
    ${not_match1}       ${json_actual_1}    ${dict_expected_2}      apple           margin_type=hours
# --- Identity Key not in expected dictionary error on lists comparison ------------------------------------------------
    ${id_key_err}       ${json_actual_2}    ${list_expected_1}      ${NONE}         ${FALSE}        what
# --- Identity Key not found in actual list dictionaries error on lists comparison -------------------------------------
    ${id_key_err_2}     ${json_actual_2}    ${list_expected_2}      ${NONE}         ${FALSE}        apple
# --- Identity Key found in actual list dictionaries but some keys mismatch error --------------------------------------
    ${not_match3}       ${json_actual_5}    ${list_expected_1}      ${NONE}         ${FALSE}        apple
# --- Top Level only mismatch on lists comparison ----------------------------------------------------------------------
    ${top_only_err}     ${json_actual_3}    ${list_expected_5}      ${NONE}         ${TRUE}         ${NONE}
# --- Top Level only mismatch on lists date comparisons ----------------------------------------------------------------

Validate Response Date Negative Tests
    [Template]      Validate Response Contains Expected Response Errors Template
#   Error                   JSON Actual             Expected Dict           Ignored Keys    Full List       Identity Key
# --- No match on date keys on single dictionary -----------------------------------------------------------------------
    ${not_match_date_1}     ${json_wo_date_none}    ${wo_example}
    ${not_match_date_2}     ${json_wo_date_bad}     ${wo_example}
    ${not_match_date_3}     ${json_wo_date_long}    ${wo_example}
    ${not_match_date_4}     ${json_wo_example}      ${wo_bad_date_example}

Validate Response List Positive Tests
    [Template]      Validate Response Contains Expected Response
#   JSON Actual         Expected Dict           Ignored Keys     Full List Validation
    ${json_actual_3}    ${list_expected_4}      ${NONE}          ${True}
    ${json_actual_2}    ${list_expected_3}      banana           ${True}
    ${json_actual_4}    ${list_expected_6}      ${NONE}          ${True}
    ${json_actual_2}    ${list_expected_6}      ${NONE}          ${True}
    ${json_actual_2}    ${list_expected_6}      whatever         ${True}

Validate Response List Negative Tests
    [Template]      Validate Response Contains Expected List Response Errors Template
#   Error               JSON Actual         Expected Dict           Ignored Keys
    ${not_match1}       ${json_actual_1}    ${dict_expected_2}      ${NONE}
    ${not_match1}       ${json_actual_1}    ${dict_expected_2}      whatever
    ${list_dict_err}    ${json_actual_2}    ${dict_expected_2}      ${NONE}
    ${not_match2}       ${json_actual_5}    ${list_expected_6}      ${NONE}

Verify Items Within Response Positive Tests
    [Template]      Validate Response Contains Expected Response
#   JSON Actual         Expected Dict           Ignored Keys      Full List Validation    Identity Key
# --- Common Case on identical Lists with Identity Key -----------------------------------------------------------------
    ${json_actual_2}    ${list_expected_1}      ${NONE}            ${False}                apple
# --- Expected list with one item inside of the Actual using Identity Key that is not unique ---------------------------
    ${json_actual_4}    ${list_expected_1}      ${NONE}            ${False}                apple
# --- Expected list with one item inside of the Actual using Identity Key that is unique -------------------------------
    ${json_actual_6}    ${list_expected_7}      ${NONE}            ${False}                id
# --- Expected item list within Actual response using Identity Key and ignoring a non existent key ---------------------
    ${json_actual_6}    ${list_expected_7}      whatever           ${False}                id
# --- Expected item within Actual response using Identity Key and ignoring a key with mismatched values ----------------
    ${json_actual_5}    ${list_expected_1}      pear               ${False}                apple


Verify Items Within Response Negative Tests
    [Template]      Verify Items Exist Within Response Errors Template
#   Error               JSON Actual         Expected Dict           Ignored Keys     Full List Validation    Identity Key
# --- Identity Key not in expected dictionary error on lists comparison ------------------------------------------------
    ${id_key_err}       ${json_actual_2}    ${list_expected_1}      ${NONE}            ${False}                what
# --- Identity Key not found in actual list dictionaries error on lists comparison -------------------------------------
    ${id_key_err_2}     ${json_actual_2}    ${list_expected_2}      ${NONE}            ${False}                apple
# --- Identity Key found in actual list dictionaries but some keys mismatch error --------------------------------------
    ${not_match3}       ${json_actual_5}    ${list_expected_1}      ${NONE}            ${False}                apple

Validate Response Number of Items Positive Tests
    [Template]      Validate Response Contains Correct Number of Items
#   JSON Actual             No of Items
    ${json_actual_6}        ${3}
    ${json_actual_2}        ${1}

Validate Response Number of Items Negative Tests
    [Template]      Validate Response Contains Correct Number of Items Errors template
#   Error               JSON Actual             No of Items
    ${no_items_err_1}   ${json_actual_2}        ${2}
    ${not_list_err_1}   ${json_actual_1}        ${1}
    ${not_list_err_1}   ${json_actual_1}        ${2}

Validate Response Contains Only Keys Listed Positive Tests
    [Template]      Validate Response Contains Expected Response Only Keys Listed
#   JSON Actual         Expected Dict           Keys List
# --- Common Case ----------------------------------------------------------------
    ${json_actual_1}    ${dict_expected_1}      ${keys_list_1}
# --- Common Case with List ------------------------------------------------------
    ${json_actual_2}    ${list_expected_1}      ${keys_list_1}
# --- List and null value --------------------------------------------------------
    ${json_actual_7}    ${list_expected_3}      ${keys_list_1}
# --- Dict with wrong value not in keys list -------------------------------------
    ${json_actual_1}    ${dict_expected_3}      ${keys_list_2}
# --- Dict with wrong value not in keys list -------------------------------------
    ${json_actual_1}    ${dict_expected_3}      ${keys_list_2}

Validate Response Contains Only Keys Listed Negative Tests
    [Template]      Validate Response Contains Expected Response Only Keys Listed Errors Template
#   Error                   JSON Actual         Expected Dict           Keys List
# --- Dict with wrong value ---------------------------------------------------------------------
    ${only_keys_err_1}      ${json_actual_1}    ${dict_expected_3}      ${keys_list_1}
# --- Dict with missing key ---------------------------------------------------------------------
    ${only_keys_err_2}      ${json_actual_1}    ${dict_expected_1}      ${keys_list_3}

Key By Key Validator Positive Tests
    [Template]      Key By Key Validator Testing Template
#   Actual Dictionary           Expected Dictionary     Expected Unmatched Keys    Ignored Keys     Unmatched Keys
    ${dict_actual_8}            ${dict_expected_8}      ${empty_list}
    ${dict_actual_9}            ${dict_expected_10}     ${unmatched_keys_9}
    ${dict_actual_9}            ${dict_expected_10}     ${unmatched_keys_10}       cat

Key By Key Validator Positive Tests - Dates
    [Template]      Key By Key Validator Testing Template
#   Actual Dictionary           Expected Dictionary     Expected Unmatched Keys    Ignored Keys     Unmatched Keys    **kwargs
    ${wo_example}               ${wo_example}           ${empty_list}
    ${wo_example_2}             ${wo_example}           ${empty_list}              margin_type=hours    margin_amt=2
    ${wo_example_none}          ${wo_example}           ${unmatched_keys_2}
    ${wo_example}               ${wo_example_none}      ${unmatched_keys_1}
    ${wo_example_bad_date}      ${wo_example}           ${unmatched_keys_7}
    ${wo_example_not_close}     ${wo_example}           ${unmatched_keys_8}

Key By Key Validator Negative Tests
    [Template]      Key By Key Validator Errors Template
#   Error String            Actual Dictionary               Expected Dictionary            Ignored Keys        Unmatched Keys
    ${bad_array_err_1}      ${dict_actual_8}                ${dict_expected_9}

Date String Comparator Positive Tests
    [Template]      Date String Comparator Template
#   Expected Date            Actual Date             Expected Unmatched Keys     Unmatched Keys
    2015-12-16T14:21:58Z    2015-12-16T14:21:58Z       ${empty_list}               ${empty_list}
    2015-12-16T14:12:58Z    2015-12-16T14:21:58Z       ${empty_list}               ${empty_list}
    2015-12-16T14:12:58Z    2015-12-16T14:21:58.05Z    ${empty_list}               ${empty_list}
    2015-12-16T14:21:58Z    2015-12-16T18:21:58Z       ${unmatched_keys_6}         ${empty_list}

Date String Comparator Negative Tests
    [Template]      Date String Comparator Errors Template
#   Error String        Expected Date           Actual Date             Expected Unmatched Keys     Unmatched Keys
    ${date_type_err}    ${NONE}                 2015-12-16T14:21:58Z    ${empty_list}               ${empty_list}
    ${date_type_err}    2015-12-16T14:21:58Z    ${NONE}                 ${empty_list}               ${empty_list}

*** Keywords ***
Validate Response Contains Expected Response Errors Template
    [Arguments]     ${error}    ${json_actual}      ${expected_dict}    ${ignored_keys}=${NONE}     ${id_key}=${EMPTY}    ${top_level}=${FALSE}    &{kwargs}
    Run Keyword And Expect Error    ${error}
    ...     Validate Response Contains Expected Response
    ...     ${json_actual}      ${expected_dict}    ${ignored_keys}     ${id_key}    ${top_level}    &{kwargs}

Validate Response Contains Expected List Response Errors Template
    [Arguments]     ${error}    ${json_actual}      ${expected_dict}    ${ignored_keys}=${NONE}   ${full_list_validation}=${True}
    Run Keyword And Expect Error    ${error}
    ...     Validate Response Contains Expected Response
    ...     ${json_actual}      ${expected_dict}    ${ignored_keys}    ${full_list_validation}

Verify Items Exist Within Response Errors Template
    [Arguments]     ${error}    ${json_actual}      ${expected_dict}    ${ignored_keys}=${NONE}     ${full_list_validation}=${True}     ${id_key}=${EMPTY}
    Run Keyword And Expect Error    ${error}
    ...     Validate Response Contains Expected Response
    ...     ${json_actual}      ${expected_dict}    ${ignored_keys}     ${full_list_validation}    ${id_key}

Validate Response Contains Correct Number of Items Errors template
    [Arguments]     ${error}    ${json_actual}      ${number_of_items}
    Run Keyword And Expect Error    ${error}
    ...     Validate Response Contains Correct Number of Items
    ...     ${json_actual}      ${number_of_items}

Validate Response Contains Expected Response Only Keys Listed Errors Template
    [Arguments]     ${error}    ${json_actual}      ${expected_dict}    ${keys_list}
    Run Keyword And Expect Error    ${error}
    ...     Validate Response Contains Expected Response Only Keys Listed
    ...     ${json_actual}      ${expected_dict}    ${keys_list}

Date String Comparator Template
    [Arguments]     ${expected_date}    ${actual_date}    ${expected_unmatched_keys}      ${unmatched_keys}=@{EMPTY}
    ${new_unmatched_keys}=      Copy List   ${unmatched_keys}
    Date String Comparator    ${expected_date}    ${actual_date}    SomeDate  ${new_unmatched_keys}
    Lists Should be Equal     ${expected_unmatched_keys}      ${new_unmatched_keys}

Date String Comparator Errors Template
    [Arguments]     ${error}    ${expected_date}    ${actual_date}    ${expected_unmatched_keys}      ${unmatched_keys}=@{EMPTY}
    ${new_unmatched_keys}=      Copy List   ${unmatched_keys}
    Run Keyword And Expect Error    ${error}
    ...                       Date String Comparator
    ...                       ${expected_date}    ${actual_date}    SomeDate  ${new_unmatched_keys}
    Lists Should be Equal     ${expected_unmatched_keys}      ${new_unmatched_keys}

Key By Key Validator Testing Template
    [Arguments]     ${actual_dictionary}  ${expected_dictionary}   ${expected_unmatched_keys}   ${ignored_keys}=${EMPTY}   ${unmatched_keys}=@{EMPTY}    &{kwargs}
    Key By Key Validator        ${actual_dictionary}    ${expected_dictionary}    ${ignored_keys}   ${unmatched_keys}    &{kwargs}
    log                         ${unmatched_keys}
    Lists Should be Equal       ${expected_unmatched_keys}      ${unmatched_keys}

Key By Key Validator Errors Template
    [Arguments]     ${error}    ${actual_dictionary}  ${expected_dictionary}   ${ignored_keys}=${EMPTY}   ${unmatched_keys}=@{EMPTY}
    Run Keyword And Expect Error    ${error}
    ...         Key By Key Validator
    ...         ${actual_dictionary}    ${expected_dictionary}    ${ignored_keys}   ${unmatched_keys}
