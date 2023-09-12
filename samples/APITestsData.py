import json

# Allows us to simply copy and paste expected results without having to change these to their python equivalents
false = False
true = True
null = None

get_basic_expected = \
    {
      "userId": 1,
      "id": 1,
      "title": "delectus aut autem",
      "completed": false
    }

get_basic_error_expected = \
    {
      "userId": 1,
      "id": 1,
      "title": "delectus aut autem",
      "completed": true
    }

get_basic_validation_error = "Error: Key(s) Did Not Match" \
            "\nUnmatched Keys List: " \
            "\n------------------" \
            "\nKey: completed" \
            "\nExpected: True" \
            "\nActual: False" \
            "\nNote: Please see differing value(s)"

post_data = \
    {
        "name": "morpheus",
        "job": "leader"
    }

post_expected = \
    {
        "name": "morpheus",
        "job": "leader",
        "id": "751",
        "createdAt": "2020-06-10T18:32:07.331Z"
    }

put_data = \
    {
        "name": "morpheus",
        "job": "zion resident"
    }

put_expected = \
    {
        "name": "morpheus",
        "job": "zion resident",
        "updatedAt": "2020-06-10T18:36:10.183Z"
    }

key_by_key_expected = \
    {
        "id": 1,
        "AssignedDate": "1234-34-45",
        "NoneField": null,
        "CreateDate": "2015-12-16T14:21:58Z",
        "CreatedByEmail": "",
        "CreatedByExternalId": "1234",
        "CreatedByFirstName": "Bob",
        "CreatedById": "318",
        "CreatedByLastName": "Ross",
        "CreatedByPhone": "(444) 444-4444"
    }

key_by_key_actual = json.dumps(key_by_key_expected)

key_by_key_expected_error = \
    {
        "id": 1,
        "AssignedDate": "1234-34-45",
        "NoneField": null,
        "CreateDate": "2015-12-16T15:22:59Z",
        "CreatedByEmail": "",
        "CreatedByExternalId": "1234",
        "CreatedByFirstName": "Bob",
        "CreatedById": "318",
        "CreatedByLastName": "Smith",
        "CreatedByPhone": "(444) 444-4444"
    }

key_by_key_error = "Error: Key(s) Did Not Match" \
            "\nUnmatched Keys List: " \
            "\n------------------" \
            "\nKey: CreateDate" \
            "\nExpected: 2015-12-16 15:22:59" \
            "\nActual: 2015-12-16 14:21:58" \
            "\nNote: Dates Not Close Enough" \
            "\n------------------" \
            "\nKey: CreatedByLastName" \
            "\nExpected: Smith" \
            "\nActual: Ross" \
            "\nNote: Please see differing value(s)"
