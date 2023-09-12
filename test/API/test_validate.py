import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
import unittest
from Zoomba.APILibrary import APILibrary
from unittest.mock import patch
from Zoomba.APILibrary import _unmatched_list_check
from dateutil import parser
from Zoomba import ZoombaError


class TestInternal(unittest.TestCase):
    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_generate_unmatched_keys_error_message_simple(self, fail):
        library = APILibrary()
        library.generate_unmatched_keys_error_message('a')
        fail.assert_called_with("Error: Key(s) Did Not Match\nUnmatched Keys List: \na\n"
                                "Note: Please see differing value(s)")

    def test_validate_response_contains_correct_number_of_items_simple(self):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', 1)

    def test_validate_response_contains_correct_number_of_items_ignore(self):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', "IGNORE")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_incorrect_number(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', b'2')
        fail.assert_called_with("Error: Did not pass number or string value, "
                                "function expects a number or string 'IGNORE'.")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_too_many_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}, {"b":2}]', 1)
        fail.assert_called_with('Error: API is returning 2 instead of the expected 1 result(s).')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_not_enough_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', 2)
        fail.assert_called_with('Error: API is returning 1 instead of the expected 2 result(s).')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_no_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('{"a":1}', 1)
        fail.assert_called_with("Error: The response is not a list:\nActual Response: \n{'a': 1}")

    def test_validate_response_contains_correct_number_of_items_string(self):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', "1")

    def test_validate_response_contains_expected_response_only_keys_listed_simple(self):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"a":1}', {"a": 1}, ["a"])

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_response_missing_key(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"b":"1"}', {"b": "1"}, ["a"])
        fail.assert_called_with("Error: The response does not contain the key 'a'")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_response_value_diff(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"a":"2"}', {"a": "1"}, ["a"])
        fail.assert_called_with("Error: The value for the key 'a' doesn't match the response:\nExpected: 1\nActual: 2")

    def test_validate_response_contains_expected_response_only_keys_listed_list_simple(self):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"a":1}]', [{"a": 1}], ["a"])

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_list_response_missing_key(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"b":"1"}]', [{"b": "1"}], ["a"])
        fail.assert_called_with("Error: The response does not contain the key 'a'")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_list_response_value_diff(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"a":"2"}]', [{"a": "1"}], ["a"])
        fail.assert_called_with("Error: The value for the key 'a' doesn't match the response:\nExpected: 1\nActual: 2")

    def test_key_by_key_validator_simple(self):
        library = APILibrary()
        library.key_by_key_validator({"a": 1}, {"a": 1})

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_collection_len_fail(self, fail):
        library = APILibrary()
        library.key_by_key_validator([{"a": 1}, {"b": 2}], {"a": 1})
        fail.assert_called_with('Error: Collections not the same length:\nActual Length: 2\nExpected Length: 1')

    def test_key_by_key_validator_simple_value_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": 2}, {"a": 1}, unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key="a", expected=1, actual=2)]

    def test_key_by_key_validator_simple_list(self):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1"]}, {"a": ["1"]})

    def test_key_by_key_validator_simple_list_multiple_values(self):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1", "2"]}, {"a": ["1", "2"]})

    def test_key_by_key_validator_list_int(self):
        library = APILibrary()
        library.key_by_key_validator({"a": [1]}, {"a": [1]})

    def test_key_by_key_validator_list_empty_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": []}, {"a": [1]}, unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key="a[0]", expected=1, actual="")]

    def test_key_by_key_validator_simple_ignored_key(self):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1"]}, {"a": ["1"]}, ["a"])

    def test_key_by_key_validator_list_int_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": [1]}, {"a": [2]}, unmatched_keys_list=unmatched)
        ZoombaError(key="a[0]", expected=2, actual=1)
        assert unmatched == [ZoombaError(key="a[0]", expected=2, actual=1)]

    def test_key_by_key_validator_list_dict_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": [{"b": 3}]}, {"a": [{"b": 4}]}, unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key='a[0].b', expected=4, actual=3)]

    def test_key_by_key_validator_list_dict_embedded_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": [{"b": [{"c": 4}]}]}, {"a": [{"b": [{"c": 5}]}]},
                                     unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key="a[0].b[0].c", expected=5, actual=4)]

    def test_key_by_key_validator_list_list_embedded_list_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": [[1], [2, [3]]]}, {"a": [[1], [2, [7]]]},
                                     unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key="a[1][0]", expected=7, actual=3)]

    def test_key_by_key_validator_list_dict_embedded_list_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": [{"b": [{"c": [4, 5]}]}]}, {"a": [{"b": [{"c": [5, 5]}]}]},
                                     unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key='a[0].b[0].c', expected=5, actual=4)]

    def test_key_by_key_validator_partial_list(self):
        library = APILibrary()
        library.key_by_key_validator(
            {"result": {"locations": [{"name": "Loc-1", "sys_id": "1"},
                                      {"name": "Loc-2", "sys_id": "2"}]}},
            {"result": {"locations": [{"name": "Loc-1", "sys_id": "1"}]}})

    def test__unmatched_list_check_parent_not_list_not_equal(self):
        unmatched = [ZoombaError(key='c', expected=5, actual=4)]
        _unmatched_list_check(unmatched, 0, "a", index=None, parent_key="b", is_list=False)
        assert unmatched == [ZoombaError(key="a.c", expected=5, actual=4)]

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_simple_none_dict(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"a": None}, {"a": {"b": "2"}})
        fail.assert_called_with("Error: Dicts do not match\nExpected: {'b': '2'}\nActual: Actual is not a valid dictionary.")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_key_not_in_actual_fail(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"b": 2, "c": 3}, {"a": 1, "c": 3})
        fail.assert_called_with("Error: Key not found in Actual\n------------------\nKey: a\nExpected: None\nActual: {'b': 2, 'c': 3}")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_list_not_same_length_fail(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1", "2"]}, {"a": ["1"]}, full_list_validation=True)
        fail.assert_called_with("Error: Arrays not the same length\nExpected: ['1']\nActual: ['1', '2']")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_list_do_not_match(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1", "2"]}, {"a": ["1", "3"]})
        fail.assert_called_with("Error: Arrays do not match\nExpected: ['1', '3']\nActual: ['1', '2']\nTip: If this is simply out of order try 'sort_list=True'")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_list_do_not_match_with_sort(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1", "2"]}, {"a": ["1", "3"]}, sort_lists=True)
        fail.assert_called_with("Error: Arrays do not match\nExpected: ['1', '3']\nActual: ['1', '2']")

    def test_key_by_key_validator_list_sort(self):
        library = APILibrary()
        library.key_by_key_validator({"a": ["1", "2"]}, {"a": ["2", "1"]}, sort_lists=True)

    def test_key_by_key_validator_list_sort_nested_dict(self):
        library = APILibrary()
        library.key_by_key_validator({"value":[{"a": ["1", "2"]}]}, {"value":[{"a": ["2", "1"]}]}, sort_lists=True)

    def test_key_by_key_validator_simple_dict(self):
        library = APILibrary()
        library.key_by_key_validator({"a": {"b": 1}}, {"a": {"b": 1}})

    def test_key_by_key_validator_simple_dict_multiple_values(self):
        library = APILibrary()
        library.key_by_key_validator({"a": {"b": 1, "c": 1}}, {"a": {"b": 1, "c": 1}})

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_dict_len_fail(self, fail):
        library = APILibrary()
        library.key_by_key_validator({"a": {"b": 1, "c": 1}}, {"a": {"b": 1}})
        fail.assert_called_with("Error: Dicts do not match\nExpected: {'b': 1}\nActual: {'b': 1, 'c': 1}")

    def test_key_by_key_validator_simple_date(self):
        library = APILibrary()
        library.key_by_key_validator({"a": "2017-08-08T05:05:05"}, {"a": "2017-08-08T05:05:05"})

    def test_key_by_key_validator_complex_date(self):
        library = APILibrary()
        library.key_by_key_validator({"a": "2017-08-08T05:05:05"}, {"a": "2017-08-08T05:05:05.234543"})

    def test_key_by_key_validator_complex_date2(self):
        library = APILibrary()
        actual_date = parser.parse("2005-03-23 08:20:09.383000")
        library.key_by_key_validator({"a": actual_date}, {"a": "2005-03-23 08:20:09"})

    def test_key_by_key_validator_tz_date(self):
        library = APILibrary()
        actual_date = parser.parse("2017-08-08T05:05:05-08:00")
        library.key_by_key_validator({"a": actual_date}, {"a": "2017-08-08T05:05:05"})

    def test_key_by_key_validator_simple_date_parse_except(self):
        library = APILibrary()
        library.key_by_key_validator({"a": "a"}, {"a": "a"})

    def test_key_by_key_validator_date_parse_except_fail(self):
        library = APILibrary()
        unmatched = []
        library.key_by_key_validator({"a": "a"}, {"a": "b"}, unmatched_keys_list=unmatched)
        assert unmatched == [ZoombaError(key="a", expected="b", actual="a")]

    def test_validate_response_contains_expected_response_simple(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"b":1}}', {"a": {"b": 1}})

    def test_validate_response_contains_expected_response_sort_nested_dict(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"value": [{"a": ["1", "2"]}]}', {"value": [{"a": ["2", "1"]}]},
                                                             sort_lists=True)

    def test_validate_response_contains_expected_response_sort_nested_dict_in_list(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"value": [{"a": [{"a":"1", "b":"2"}, {"c":"3", "d":"4"}]}]}',
                                                             {"value": [{"a": [{"c":"3", "d":"4"}, {"a":"1", "b":"2"}]}]},
                                                             sort_lists=True)

    def test_validate_response_contains_expected_response_simple_list(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"id":1}, {"id":2}]', [{"id": 1}, {"id": 2}])

    def test_validate_response_contains_expected_response_list_with_identity_key(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":1}, {"a":2}]', [{"a": 1}, {"a": 2}], identity_key="a")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_simple_fail(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response(None, {"a": {"b": 1}})
        fail.assert_called_with("The Actual Response is Empty.")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_empty_dict_fail(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('{}', {"a": {"b": 1}})
        fail.assert_called_with("The Actual Response is Empty.")

    def test_validate_response_contains_expected_response_ignored(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"b":1},"c":2}', {"a": {"b": 1}, "c": 3},
                                                             ignored_keys=["c"])

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_unmatched(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"b":1},"c":2}', {"a": {"b": 1}, "c": 3})
        fail.assert_called_with('Error: Key(s) Did Not Match\nUnmatched Keys List: \n------------------\nKey: c\nExpected: '
                                '3\nActual: 2\nNote: Please see differing value(s)')

    def test_validate_response_contains_expected_response_full_list(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":{"b":1}}]', [{"a": {"b": 1}}],
                                                             full_list_validation=True)

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_empty_list_fail(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[]', {"a": {"b": 1}})
        fail.assert_called_with("The Actual Response is Empty.")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_list_unmatched(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":{"b":1},"c":2}]', [{"a": {"b": 1}, "c": 3}],
                                                             full_list_validation=True)
        fail.assert_called_with("Error: Key(s) Did Not Match\nUnmatched Keys List: \n------------------\nKey: c\nExpected: 3\nActual: 2"
                                "\n------------------\nFull List Breakdown: \nExpected: [{'a': {'b': 1}, 'c': 3}]"
                                "\nActual: [{'a': {'b': 1}, 'c': 2}]\nNote: Please see differing value(s)")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_identity_key_simple(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":{"b":1},"c":2}]', [{"a": {"b": 1}, "c": 3}],
                                                             identity_key="a")
        fail.assert_called_with('Error: Key(s) Did Not Match\nUnmatched Keys List: \n------------------\nKey: c\nExpected: '
                                '3\nActual: 2\nNote: Please see differing value(s)')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_list_no_identity_key_fail(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":{"b":1},"c":2}]', [{"a": {"b": 1}, "c": 3}],
                                                             identity_key="string")
        fail.assert_called_with('KeyError: "string" Key was not in the response')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_list_unmatched_identity_key_fail(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":2,"c":2}]', [{"a": 1, "c": 3}],
                                                             identity_key="a")
        fail.assert_called_with("Error: Item was not within the response:\n{'a': 1, 'c': 3}")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_list_unmatched_identity_key_continue_simple(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response('[{"a":2,"c":2}, {"a":1,"c":2}]', [{"a": 1, "c": 3}],
                                                             identity_key="a")
        fail.assert_called_with('Error: Key(s) Did Not Match\nUnmatched Keys List: \n------------------\n'
                                'Key: c\nExpected: 3\nActual: 2\nNote: Please see differing value(s)')

    def test_validate_response_contains_expected_response_simple_date_compare(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"date":"2005-03-23"}}', {"a": {"date": "2005-03-23"}})

    def test_validate_response_contains_expected_response_extended_date_compare(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"date":"2008-06-16 06:19:26"}}', {"a": {"date":"2008-06-16 06:19:26"}})

    def test_validate_response_contains_expected_response_extended_date_compare2(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"date":"2005-03-23 08:20:09"}}', {"a": {"date":"2005-03-23 08:20:09.383000"}})

    def test_validate_response_contains_expected_response_extended_date_compare_offset(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"date":"2008-06-16 06:19:26"}}', {"a": {"date":"2008-06-16 06:20:26"}})

    def test_validate_response_contains_expected_response_extended_date_compare_timezone_data(self):
        library = APILibrary()
        library.validate_response_contains_expected_response('{"a":{"date":"2008-06-16T06:19:26-07:00"}}', {"a": {"date":"2008-06-16 06:20:26"}})

    def test_validate_response_contains_expected_response_date_already_datetime(self):
        library = APILibrary()
        expected = datetime(2005, 3, 23, 8, 20, 9, 383000)
        library.validate_response_contains_expected_response('{"a":{"date":"2005-03-23 08:21:09"}}', {"a": {"date":expected}})

    def test_validate_response_contains_expected_response_date_already_datetime_with_tzdata(self):
        library = APILibrary()
        expected = datetime(2005, 3, 23, 8, 20, 9, 383000)
        library.validate_response_contains_expected_response('{"a":{"date":"2005-03-23 08:20:10-07:00"}}', {"a": {"date":expected}})
