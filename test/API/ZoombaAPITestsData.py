
# ---------------------- JSON Examples for use on the Validator Testing ------------------------------------------------

json_actual_1 = """
    {
        "apple": "cat",
        "banana": "dog",
        "pear": "fish"
    }
"""

json_actual_2 = """
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": "fish"
        }
    ]
"""

json_actual_3 = """
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": {"color": "green", "size": "small"}
        }
    ]
"""

json_actual_4 = """
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": "fish"
        },
        {
            "apple": "cat",
            "banana": "mice",
            "pear": "bird"
        },
        {
            "apple": "dog",
            "banana": "mice",
            "pear": "cat"
        }
    ]
"""

json_actual_5 = """
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": "bird"
        }
    ]
"""

json_actual_6 = """
    [
        {
            "id": "1",
            "banana": "dog",
            "pear": "fish"
        },
        {
            "id": "2",
            "banana": "mice",
            "pear": "bird"
        },
        {
            "id": "3",
            "banana": "mice",
            "pear": "cat"
        }
    ]
"""

json_actual_7 = """
    [
        {
            "apple": "cat",
            "banana": null,
            "pear": "fish"
        }
    ]
"""

dict_actual_8 = \
    {
       "apple": "cat",
       "strawberry":
       [
          "dog",
          "cat",
          "bird",
          "elephant",
       ],
       "bananas":
       [
          "red",
          "blue",
          "green",
          "yellow",
       ],
       "pear":
       [
          "pigeon"
       ]
   }

dict_actual_9 = \
    {
        "apple": "cat",
        "strawberry":
        [
            {
                "dog": "wags",
                "cat": "meow"
            }
        ]
    }
# ------------------ List and Dictionary objects for use on Validator Testing ------------------------------------------

dict_expected_1 = \
    {
        "apple": "cat",
        "banana": "dog",
        "pear": "fish"
    }
dict_expected_2 = \
    {
        "apple": "cat",
        "banana": "dog",
        "pear": "bird"
    }

dict_expected_3 = \
    {
        "apple": "elephant",
        "banana": "dog",
        "pear": "fish"
    }

list_expected_1 = \
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": "fish"
        }
    ]

list_expected_2 = \
    [
        {
            "pear": "fish",
            "apple": "elephant",
            "banana": "dog"
        }
    ]

list_expected_3 = \
    [
        {
            "apple": "cat",
            "banana": None,
            "pear": "fish"
        }
    ]

list_expected_4 = \
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": {"color": "green", "size": "small"}
        }
    ]

list_expected_5 = \
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": {"color": "green", "size": "large"}
        }
    ]

list_expected_6 = \
    [
        {
            "apple": "cat",
            "banana": "dog",
            "pear": "fish"
        },
        {
            "apple": "cat",
            "banana": "mice",
            "pear": "bird"
        },
        {
            "apple": "dog",
            "banana": "mice",
            "pear": "cat"
        }
    ]

list_expected_7 = \
    [
        {
            "id": "2",
            "banana": "mice",
            "pear": "bird"
        }
    ]

dict_expected_8 = \
    {
       "apple": "cat",
       "strawberry":
       [
          "dog",
          "cat",
          "bird",
          "elephant",
       ],
       "bananas":
       [
          "red",
          "blue",
          "green",
          "yellow",
       ],
       "pear":
       [
          "pigeon",
       ]
   }

dict_expected_9 = \
    {
       "apple": "apple",
       "strawberry":
       [
          "str",
          "aw",
          "ber",
          "ry",
       ],
       "bananas":
       [
          "ba",
          "na",
          "na",
          "s",
       ],
       "pear":
       [
          "pear",
       ]
   }

dict_expected_10 = \
{
    "apple": "cat",
    "strawberry": [
        {
            "dog": 9854,
            "cat": "purr"
        }
    ]
}

keys_list_1 = ["apple", "banana"]

keys_list_2 = ["banana", "pear"]

keys_list_3 = ["apple", "orange"]

empty_list = []

unmatched_keys_1 = ["------------------\nKey: AssignedDate\nExpected: None\nActual: 2015-12-16T14:21:58Z"]
unmatched_keys_2 = ["------------------\nKey: AssignedDate\nExpected: 2015-12-16T14:21:58Z\nActual: None"]
unmatched_keys_3 = ["The Expected and Actual values for this date are not of the same type\nKey: SomeDate\n"
                     "Actual: 2015-12-16T14:21:58Z"]
unmatched_keys_4 = ["The Expected and Actual values for this date are not of the same type\nKey: SomeDate\n"
                     "Expected: 2015-12-16T14:21:58Z"]
unmatched_keys_5 = ["Date time parsing failed for key: SomeDate\n"
                     "Expected: 2015-12-16T14:21:58Z\nActual: 1234-34-45"]
unmatched_keys_6 = ["------------------\nKey: SomeDate\nExpected: 2015-12-16 14:21:58"
                    "\nActual: 2015-12-16 18:21:58\nNote: Dates Not Close Enough"]
unmatched_keys_7 = ["------------------\nKey: AssignedDate\nNote: Actual Date Not Correct Format\n"
                     "Expected Formats: %Y-%m-%dT%H:%M:%S\n                  %Y-%m-%dT%H:%M:%SZ\n"
                     "                  %Y-%m-%dT%H:%M:%S.%f\n                  %Y-%m-%dT%H:%M:%S.%fZ\n"
                     "Date: 1234-34-45"]
unmatched_keys_8 = ["------------------\nKey: AssignedDate\nExpected: 2015-12-16 14:21:58"
                    "\nActual: 2015-12-16 14:10:58\nNote: Dates Not Close Enough"]
unmatched_keys_9 = \
            [
                "------------------\nKey: strawberry[0].dog\nExpected: 9854\nActual: wags",
                "------------------\nKey: strawberry[0].cat\nExpected: purr\nActual: meow"
            ]
unmatched_keys_10 = \
            [
                "------------------\nKey: strawberry[0].dog\nExpected: 9854\nActual: wags"
            ]
unmatched_keys_11 = ["------------------\nKey: SomeDate\nNote: Date Not Correct Format\n"
                     "Expected Formats: %Y-%m-%dT%H:%M:%S'\n                  %Y-%m-%dT%H:%M:%SZ,"
                     "                  %Y-%m-%dT%H:%M:%S.%f\n                  %Y-%m-%dT%H:%M:%S.%fZ\n"
                     "Date: 1234-34-45'"]
# ---------------- Error Messages --------------------------------------------------------------------------------------

not_match1 = "Error: Key(s) Did Not Match" \
            "\nUnmatched Keys List: " \
            "\n------------------" \
            "\nKey: pear" \
            "\nExpected: bird" \
            "\nActual: fish" \
            "\nNote: Please see differing value(s)"
not_match2 = "Error: Key(s) Did Not Match" \
             "\nUnmatched Keys List: " \
             "\n------------------" \
             "\nKey: pear" \
             "\nExpected: fish" \
             "\nActual: bird" \
             "\n------------------" \
             "\nFull List Breakdown: " \
             "\nExpected: [{'apple': 'cat', 'banana': 'dog', 'pear': 'fish'}, {'apple': 'cat', 'banana': 'mice', 'pear': 'bird'}, {'apple': 'dog', 'banana': 'mice', 'pear': 'cat'}]" \
             "\nActual: [{'apple': 'cat', 'banana': 'dog', 'pear': 'bird'}]" \
             "\nNote: Please see differing value(s)"
not_match3 = "Error: Key(s) Did Not Match" \
            "\nUnmatched Keys List: " \
            "\n------------------" \
            "\nKey: pear" \
            "\nExpected: fish" \
            "\nActual: bird" \
            "\nNote: Please see differing value(s)"

not_match_date_1 = "Error: Key(s) Did Not Match" \
                   "\nUnmatched Keys List: " \
                   "\n------------------" \
                   "\nKey: AssignedDate" \
                   "\nExpected: 2015-12-16T14:21:58Z" \
                   "\nActual: None" \
                   "\nNote: Please see differing value(s)"

not_match_date_2 = "Error: Key(s) Did Not Match" \
                   "\nUnmatched Keys List: " \
                   "\n------------------" \
                   "\nKey: AssignedDate" \
                   "\nNote: Actual Date Not Correct Format" \
                   "\nExpected Formats: %Y-%m-%dT%H:%M:%S" \
                   "\n                  %Y-%m-%dT%H:%M:%SZ" \
                   "\n                  %Y-%m-%dT%H:%M:%S.%f" \
                   "\n                  %Y-%m-%dT%H:%M:%S.%fZ" \
                   "\nDate: 1234-34-45" \
                   "\nNote: Please see differing value(s)"

not_match_date_3 = "Error: Key(s) Did Not Match" \
                   "\nUnmatched Keys List: " \
                   "\n------------------" \
                   "\nKey: AssignedDate" \
                   "\nExpected: 2015-12-16 14:21:58" \
                   "\nActual: 2015-12-16 14:10:58" \
                   "\nNote: Dates Not Close Enough" \
                   "\nNote: Please see differing value(s)"

id_key_err = 'KeyError: "what" Key was not in the response'

id_key_err_2 = "Error: Item was not within the response:" \
               "\n{'pear': 'fish', 'apple': 'elephant', 'banana': 'dog'}"
top_only_err = "Error: Key(s) Did Not Match" \
               "\nUnmatched Keys List: " \
               "\n------------------" \
               "\nKey: size" \
               "\nExpected: large" \
               "\nActual: small" \
               "\n------------------" \
               "\nFull List Breakdown: " \
               "\nExpected: [{'apple': 'cat', 'banana': 'dog', 'pear': {'color': 'green', 'size': 'large'}}]" \
               "\nActual: [{'apple': 'cat', 'banana': 'dog', 'pear': {'color': 'green', 'size': 'small'}}]" \
               "\nNote: Please see differing value(s)"

list_dict_err = "Error: Collections not the same length:" \
                "\nActual Length: 3" \
                "\nExpected Length: 5"

only_keys_err_1 = "Error: The value for the key 'apple' doesn't match the response:" \
                  "\nExpected: elephant" \
                  "\nActual: cat"

only_keys_err_2 = "Error: The response does not contain the key 'orange'"

no_items_err_1 = "Error: API is returning 1 instead of the expected 2 result(s)."

not_list_err_1 = "Error: The response is not a list:" \
                 "\nActual Response: " \
                 "\n{'apple': 'cat', 'banana': 'dog', 'pear': 'fish'}"

bad_value_err = "Error: The value for the key you provided doesn't match the response:" \
                "\nExpected: dog" \
                "\nActual: cat"

bad_key_err = "KeyError: 'The response does not contain the key you provided: mango'"

date_type_err = "TypeError: strptime() argument 1 must be str, not None"

empty_resp_err = "The Actual Response is Empty."

bad_array_err_1 = "Error: Arrays do not match" \
                "\nExpected: ['str', 'aw', 'ber', 'ry']" \
                "\nActual: ['dog', 'cat', 'bird', 'elephant']" \
                "\nTip: If this is simply out of order try 'sort_list=True'"
# -------------- Date Methods Test Data --------------------------------------------------------------------------------
json_wo_date_none = """
    {
        "AssignedDate": null,
        "NoneField": null,
        "CreateDate": "2015-12-16T14:21:58Z",
        "CreatedByEmail": "",
        "CreatedByExternalId": "360API_ExtID_User318",
        "CreatedByFirstName": "MyCompanyOnlyRight",
        "CreatedById": "318",
        "CreatedByLastName": "GETWOUserWith",
        "CreatedByPhone": "(444) 444-4444"
    }
"""

json_wo_date_bad = """
    {
        "AssignedDate": "1234-34-45",
        "NoneField": null,
        "CreateDate": "2015-12-16T14:21:58Z",
        "CreatedByEmail": "",
        "CreatedByExternalId": "360API_ExtID_User318",
        "CreatedByFirstName": "MyCompanyOnlyRight",
        "CreatedById": "318",
        "CreatedByLastName": "GETWOUserWith",
        "CreatedByPhone": "(444) 444-4444"
    }
"""

json_wo_date_long = """
    {
        "AssignedDate": "2015-12-16T14:10:58Z",
        "NoneField": null,
        "CreateDate": "2015-12-16T14:21:58Z",
        "CreatedByEmail": "",
        "CreatedByExternalId": "360API_ExtID_User318",
        "CreatedByFirstName": "MyCompanyOnlyRight",
        "CreatedById": "318",
        "CreatedByLastName": "GETWOUserWith",
        "CreatedByPhone": "(444) 444-4444"
    }
"""


wo_example = \
{
    "AssignedDate": "2015-12-16T14:21:58Z",
    "NoneField": None,
    "CreateDate": "2015-12-16T14:21:58Z",
    "CreatedByEmail": "",
    "CreatedByExternalId": "360API_ExtID_User318",
    "CreatedByFirstName": "MyCompanyOnlyRight",
    "CreatedById": "318",
    "CreatedByLastName": "GETWOUserWith",
    "CreatedByPhone": "(444) 444-4444"
}

wo_example_2 = \
{
    "AssignedDate": "2015-12-16T16:21:58Z",
    "NoneField": None,
    "CreateDate": "2015-12-16T14:21:58Z",
    "CreatedByEmail": "",
    "CreatedByExternalId": "360API_ExtID_User318",
    "CreatedByFirstName": "MyCompanyOnlyRight",
    "CreatedById": "318",
    "CreatedByLastName": "GETWOUserWith",
    "CreatedByPhone": "(444) 444-4444"
}

wo_example_none = \
{
    "AssignedDate": None,
    "NoneField": None,
    "CreateDate": "2015-12-16T14:21:58Z",
    "CreatedByEmail": "",
    "CreatedByExternalId": "360API_ExtID_User318",
    "CreatedByFirstName": "MyCompanyOnlyRight",
    "CreatedById": "318",
    "CreatedByLastName": "GETWOUserWith",
    "CreatedByPhone": "(444) 444-4444"
}


wo_example_bad_date = \
{
    "AssignedDate": "1234-34-45",
    "NoneField": None,
    "CreateDate": "2015-12-16T14:21:58Z",
    "CreatedByEmail": "",
    "CreatedByExternalId": "360API_ExtID_User318",
    "CreatedByFirstName": "MyCompanyOnlyRight",
    "CreatedById": "318",
    "CreatedByLastName": "GETWOUserWith",
    "CreatedByPhone": "(444) 444-4444"
}


wo_example_not_close = \
{
    "AssignedDate": "2015-12-16T14:10:58Z",
    "NoneField": None,
    "CreateDate": "2015-12-16T14:21:58Z",
    "CreatedByEmail": "",
    "CreatedByExternalId": "360API_ExtID_User318",
    "CreatedByFirstName": "MyCompanyOnlyRight",
    "CreatedById": "318",
    "CreatedByLastName": "GETWOUserWith",
    "CreatedByPhone": "(444) 444-4444"
}
