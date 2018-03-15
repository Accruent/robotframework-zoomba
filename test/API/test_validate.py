import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.APILibrary import APILibrary
import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestInternal(unittest.TestCase):
    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_generate_unmatched_keys_error_message_simple(self, fail):
        library = APILibrary()
        library.generate_unmatched_keys_error_message('a')
        assert fail.called_with("""Key(s) Did Not Match: a Please see differing value(s)""")

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
        fail.assert_called_with("Did not pass number or string value, function expects a number or string 'IGNORE'.")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_too_many_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}, {"b":2}]', 1)
        fail.assert_called_with('API is returning 2 instead of the expected 1 result(s).')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_not_enough_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('[{"a":1}]', 2)
        fail.assert_called_with('API is returning 1 instead of the expected 2 result(s).')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_correct_number_of_items_no_list(self, fail):
        library = APILibrary()
        library.validate_response_contains_correct_number_of_items('{"a":1}', 1)
        fail.assert_called_with("The response is not a list:\nActual Response:\n{'a': 1}")

    def test_validate_response_contains_expected_response_only_keys_listed_simple(self):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"a":1}', {"a":1}, ["a"])

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_response_missing_key(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"b":"1"}', {"b":"1"}, ["a"])
        fail.assert_called_with("The response does not contain the key 'a'")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_response_value_diff(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('{"a":"2"}', {"a":"1"}, ["a"])
        fail.assert_called_with("The value for the key 'a' doesn't match the response:\nExpected: 1\nActual: 2")

    def test_validate_response_contains_expected_response_only_keys_listed_list_simple(self):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"a":1}]', [{"a":1}], ["a"])

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_list_response_missing_key(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"b":"1"}]', [{"b":"1"}], ["a"])
        fail.assert_called_with("The response does not contain the key 'a'")

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_validate_response_contains_expected_response_only_keys_listed_list_response_value_diff(self, fail):
        library = APILibrary()
        library.validate_response_contains_expected_response_only_keys_listed('[{"a":"2"}]', [{"a":"1"}], ["a"])
        fail.assert_called_with("The value for the key 'a' doesn't match the response:\nExpected: 1\nActual: 2")

    def test_key_by_key_validator_simple(self):
        library = APILibrary()
        library.key_by_key_validator({"a":1}, {"a":1})

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_key_by_key_validator_collection_len_fail(self, fail):
        library = APILibrary()
        library.key_by_key_validator([{"a":1}, {"b":2}], {"a":1})
        fail.assert_called_with('Collections not the same length:\nActual length: 2\nExpected length 1')

    def test_key_by_key_validator_simple_list(self):
        library = APILibrary()
        library.key_by_key_validator({"a":["1"]}, {"a":["1"]})

    @unittest.expectedFailure
    def test_key_by_key_validator_simple_list(self):
        library = APILibrary()
        library.key_by_key_validator({"a":[1]}, {"a":[1]})














