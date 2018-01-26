import datetime
import json

from RequestsLibrary import RequestsLibrary
from dateutil.parser import parse
from urllib3.exceptions import InsecureRequestWarning
from requests.packages import urllib3
from robot.libraries.BuiltIn import BuiltIn


class APILibrary(object):
    """Zoomba API Library
        This class is the base Library used to generate automated API Tests in the Robot Automation Framework.
        It has been generated to accommodate the RESTful API design pattern.
    """
    def __init__(self):
        self.suppress_warnings=False

    def supress_insecure_request_warnings(self, suppress="True"):
        """Suppress Insecure Request Warnings. This keyword suppress or un-suppresses insecure request warnings\n
        suppress: (bool) True/False to suppress warnings, default is True\n
        Examples:
        | Suppress Insecure Request Warnings                       #Supresses Insecure Request Warnings
        | Suppress Insecure Request Warnings | suppress=True |     #Supresses Insecure Request Warnings
        | Suppress Insecure Request Warnings | False |    #Does Not Supresses Insecure Request Warnings
        """
        if "FALSE" in suppress.upper():
            self.warnings = False
        else:
            self.warnings = True

    def call_get_request(self, headers=None, endpoint=None, fullstring=None):
        """ Generate a GET Request. This Keyword is basically a wrapper for get_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
            along with any query parameters.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("getapi", endpoint, headers)
        resp = requests_lib.get_request("getapi", fullstring)
        return resp

    def call_post_request(self, headers=None, endpoint=None, fullstring=None, data=None, files=None):
        """ Generate a POST Request. This Keyword is basically a wrapper for post_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            files: (json) A JSON object that sends in the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("postapi", endpoint, headers)
        resp = requests_lib.post_request("postapi", fullstring, data, files=files)
        return resp

    def call_delete_request(self, headers=None, endpoint=None, fullstring=None, data=None):
        """ Generate a DELETE Request. This Keyword is basically a wrapper for delete_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if not self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("deleteapi", endpoint, headers)
        resp = requests_lib.delete_request("deleteapi", fullstring, data)
        return resp

    def call_patch_request(self, headers=None, endpoint=None, fullstring=None, data=None):
        """ Generate a PATCH Request. This Keyword is basically a wrapper for patch_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if not self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("patchapi", endpoint, headers)
        resp = requests_lib.patch_request("patchapi", fullstring, data)
        return resp

    def call_put_request(self, headers=None, endpoint=None, fullstring=None, data=None):
        """ Generate a PUT Request. This Keyword is basically a wrapper for put_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if not self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("putapi", endpoint, headers)
        resp = requests_lib.put_request("putapi", fullstring, data)
        return resp

    def create_connection(self, endpoint, method, data, headers=None):
        """ Opens a connection to an Application Endpoint. This Keyword is used commonly as part of a Login or Initial
            Authentication request. Given it's similarities to a pure post request, this could be deprecated in the near
            future.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.\n
        """
        if not self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib = RequestsLibrary()
        requests_lib.create_session("postapi", endpoint, headers)
        resp = requests_lib.post_request("postapi", method, data)
        return resp

    def validate_response_contains_expected_response(self, json_actual_response, expected_response_dict,
                                                     ignored_keys=None, full_list_validation=False, identity_key="",
                                                     **kwargs):
        """ This is the most used method for validating Request responses from an API against a supplied
            expected response. It performs an object to object comparison between two json objects, and if that fails,
            a more in depth method is called to find the exact discrepancies between the values of the provided objects.
            Additionally, a list of keys to ignore on the comparison may be supplied, for keys' values to be ignored./n

            json_actual_response: (request response object) The response from an API.\n
            expected_response_dict: (json) The expected response, in json format.\n
            ignored_keys: (strings list) A list of strings of the keys to be ignored on the validation.\n
            **kwargs: (dict) Currently supported kwargs are margin_type and margin_amt\n
            margin_type: (string) The type of unit of time to be used to generate a delta for the date comparisons.\n
            margin_amt: (string/#) The amount of units specified in margin_type to allot for difference between dates.\n
            return: There is no actual returned output, other than error messages when comparisons fail.\n
        """
        if not json_actual_response:
            assert False, "The Actual Response is Empty."
        else:
            actual_response_dict = json.loads(json_actual_response)
            unmatched_keys_list = []
        if type(actual_response_dict) is not list and actual_response_dict:
            if actual_response_dict == expected_response_dict:
                assert True
            else:
                self.key_by_key_validator(actual_response_dict, expected_response_dict, ignored_keys,
                                          unmatched_keys_list, **kwargs)
                self.generate_unmatched_keys_error_message(unmatched_keys_list)
                return
        elif type(actual_response_dict) is list and actual_response_dict:
            if full_list_validation:
                if actual_response_dict == expected_response_dict:
                    assert True
                else:
                    for actual_item, expected_item in zip(actual_response_dict, expected_response_dict):
                        self.key_by_key_validator(actual_item, expected_item, ignored_keys, unmatched_keys_list,
                                                  **kwargs)
                    if len(unmatched_keys_list) > 0:
                        BuiltIn().log("Responses didn't match:"
                                   "\nActual:\n" + str(actual_response_dict) +
                                   "\nExpected:\n" + str(expected_response_dict) + "\n", console=True)
                        self.generate_unmatched_keys_error_message(unmatched_keys_list)
                    return
            else:
                for exp_item in expected_response_dict:
                    for actual_item in actual_response_dict:
                        if exp_item[identity_key] == actual_item[identity_key]:
                            self.key_by_key_validator(actual_item, exp_item, ignored_keys, unmatched_keys_list,
                                                      **kwargs)
                            self.generate_unmatched_keys_error_message(unmatched_keys_list)
                            break
                        elif actual_response_dict[-1] == actual_item:
                            assert False, 'Item was not within the response:\n' + str(exp_item)
                        else:
                            continue
        else:
            assert False, "The Actual Response is Empty."

    def validate_response_contains_expected_response_only_keys_listed(self, json_actual_response, expected_response,
                                                                      key_list):
        """ This keyword is used for validating that a specific set of key-value pairs are contained on Request
            responses from an API.\n
            json_actual_response: (request response object) The response from an API.\n
            jsonExpectedResponse: (json) The expected response, in json format.\n
            key_list: (strings list) A list of strings of the keys to be included on the validation.\n
            return: There is no actual returned output, other than error messages when comparisons fail.\n
        """
        actual_response_dict = json.loads(json_actual_response)
        if type(actual_response_dict) is not list:
            for expected_key in key_list:
                assert expected_key in actual_response_dict, \
                    "The response does not contain the key '" + expected_key + "'"
                assert actual_response_dict[expected_key] == expected_response[expected_key], \
                    "The value for the key '" + expected_key + "' doesn't match the response:" + \
                    "\nExpected: " + expected_response[expected_key] +\
                    "\nActual: " + actual_response_dict[expected_key]
            return
        elif type(actual_response_dict) is list:
            for expected_key in key_list:
                assert expected_key in actual_response_dict[0], \
                    "The response does not contain the key '" + expected_key + "'"
                assert actual_response_dict[0][expected_key] == expected_response[0][expected_key], \
                    "The value for the key '" + expected_key + "' doesn't match the response:" + \
                    "\nExpected: " + expected_response[0][expected_key] + \
                    "\nActual: " + actual_response_dict[0][expected_key]
            return

    def validate_response_contains_correct_number_of_items(self, json_actual_response, number_of_items):
        """ This keyword is used to validate the number of returned items on Request responses from an API.\n
            json_actual_response: (request response object) The response from an API.\n
            number_of_items: (integer) The expected number of items.\n
            return: There is no actual returned output, other than error messages when comparisons fail.\n
        """
        actual_response_dict = json.loads(json_actual_response)
        if type(number_of_items) is str:
            number_of_items = number_of_items.upper()
            if number_of_items == "IGNORE":
                return True
            else:
                assert False, "Passed a unicode or string value, function expects a number or string 'IGNORE'."

        if type(actual_response_dict) is list:
            assert len(actual_response_dict) == number_of_items, 'API is returning ' + str(
                len(actual_response_dict)) + ' instead of the expected ' + str(number_of_items) + ' result(s).'
        else:
            raise TypeError("The response is not a list:\nActual Response:\n" + str(actual_response_dict))

    def key_by_key_validator(self, actual_dictionary, expected_dictionary, ignored_keys=None, unmatched_keys_list=None,
                             **kwargs):
        """ This method is used to find and verify the value of every key in the expectedItem dictionary when compared
            against a single dictionary actual_item, unless any keys are included on the ignored_keys array./n

            actual_item: (array of dictionaries) The list of dictionary items extracted from a json Response.\n
            ExpectedItem: (dictionary) The expected item with the key to be validated.\n
            ignored_keys: (strings list) A list of strings of the keys to be ignored on the validation.\n
            **kwargs: (dict) Currently supported kwargs are margin_type and margin_amt\n
            margin_type: (string) The type of unit of time to be used to generate a delta for the date comparisons.\n
            margin_amt: (string/#) The amount of units specified in margin_type to allot for difference between dates.\n
            return: (boolean) If the method completes successfully, it returns True. Appropriate error messages are
            returned otherwise.\n
        """
        assert len(actual_dictionary) == len(expected_dictionary), "Collections not the same length:"\
                                                                   "\nActual length: " + str(len(actual_dictionary)) +\
                                                                   "\nExpected length " + str(len(expected_dictionary))
        for key, value in expected_dictionary.items():
            if ignored_keys and key in ignored_keys:
                continue
            else:
                assert key in actual_dictionary,\
                    "Key not found in Actual : " + str(actual_dictionary) + " Key: " + str(key)
                if isinstance(value, list):
                    assert len(value) == len(actual_dictionary[key]), "Arrays not the same length:" + \
                                                                      "\nExpected: " + str(value) + \
                                                                      "\nActual: " + str(actual_dictionary[key])
                    for item in value:
                        if isinstance(item, str):
                            assert value == actual_dictionary[key],   "Arrays do not match:" + \
                                                                      "\nExpected: " + str(value) + \
                                                                      "\nActual: " + str(actual_dictionary[key])
                            continue
                        actual_item = actual_dictionary[key][value.index(item)]
                        self.key_by_key_validator(actual_item, item, ignored_keys, unmatched_keys_list, **kwargs)
                elif isinstance(value, dict):
                    assert len(value) == len(actual_dictionary[key]), "Dicts do not match:" + \
                                                                      "\nExpected: " + str(value) + \
                                                                      "\nActual: " + str(actual_dictionary[key])
                    self.key_by_key_validator(actual_dictionary[key], expected_dictionary[key],
                                              ignored_keys, unmatched_keys_list, **kwargs)
                elif isinstance(expected_dictionary[key], str) and not expected_dictionary[key].isdigit():
                    try:
                        parse(expected_dictionary[key])
                        self.date_string_comparator(value, actual_dictionary[key], key, unmatched_keys_list, **kwargs)
                    except (ValueError, TypeError):
                        if value == actual_dictionary[key]:
                            continue
                        else:
                            unmatched_keys_list.append(("------------------\n" + "Key: " + str(key),
                                                        "Expected: " + str(value),
                                                        "Actual: " + str(actual_dictionary[key])))
                elif value == actual_dictionary[key]:
                    continue
                else:
                    unmatched_keys_list.append(("------------------\n" + "Key: " + str(key), "Expected: " + str(value),
                                                "Actual: " + str(actual_dictionary[key])))
        return True

    def date_string_comparator(self, expected_date, actual_date, key, unmatched_keys_list, **kwargs):
        """This Method is used to validate a single property on a JSON object of the Date Type.
        It Validates for any the following Date Formats:
        %Y-%m-%dT%H:%M:%S, %Y-%m-%dT%H:%M:%SZ, %Y-%m-%dT%H:%M:%S.%f, %Y-%m-%dT%H:%M:%S.%fZ

        expected_date: (string) The Expected date string the key being validated.\n
        actual_date: (string) The Actual date string of the key being validated.\n
        key: (string) The key being validated.\n
        unmatched_keys_list (list): List of keys that are unvalidated - to be passed to error handling method.
        **kwargs: (dict) Currently supported kwargs are margin_type and margin_amt\n
        margin_type: (string) The type of unit of time to be used to generate a delta for the date comparisons.\n
        margin_amt: (string/#) The amount of units specified in margin_type to allot for difference between dates.\n
        """
        if expected_date == actual_date:
            return
        else:
            expected_utc = _date_format(expected_date, key, unmatched_keys_list, "Expected")
            actual_utc = _date_format(actual_date, key, unmatched_keys_list, "Actual")
            if expected_utc and actual_utc:
                self.date_comparator(expected_utc, actual_utc, key, unmatched_keys_list, **kwargs)

    def date_comparator(self, expected_date, actual_date, key, unmatched_keys_list, margin_type="minutes", margin_amt=10):
        """This method compares two date values, given a certain margin type(minutes, seconds, etc),
        and a margin amount (int). If the two dates are not within the margin amount for the margin type, I.E. within
        10 minutes of difference, it asserts False, and returns an error message.

        expected_date: (date) The Expected date value of the key being validated.\n
        actual_date: (date) The Actual date value of the key being validated.\n
        key: (string) The key being validated.\n
        unmatched_keys_list: (list) List of Date keys that are not within the accepted margin_type
        and margin_amt resolution\n
        margin_type: (string) The type of unit of time to be used to generate a delta for the date comparisons.\n
        margin_amt: (integer) The amount of units specified in margin_type to allot for difference between dates.\n
        """
        arg_dict = {margin_type: int(margin_amt)}
        margin = datetime.timedelta(**arg_dict)
        if expected_date - margin <= actual_date and actual_date <= expected_date + margin:
            return
        else:
            unmatched_keys_list.append(("------------------\n" + "Dates Not Close Enough\nKey: " + str(key),
                                        "Expected: " + str(expected_date),
                                        "Actual: " + str(actual_date)))

    def generate_unmatched_keys_error_message(self, unmatched_keys):
        """ This method is only used as an internal call from other validating methods to generate an error string
            containing every unmatched key when a validation fails.\n
            unmatchedKeys: (array of key/value pairs) An array containing the unmatched keys during a validation.\n
        """
        if len(unmatched_keys) > 0:
            keys_error_msg = "Key(s) Did Not Match:\n"
            for key_error_tuple in unmatched_keys:
                for key_error in key_error_tuple:
                    keys_error_msg += str(key_error) + "\n"
            assert False, keys_error_msg + "\nPlease see differing value(s)"


def _date_format(date_string, key, unmatched_keys_list, date_type, date_format=None):
    formatted_date = None
    if date_format is None:
        try:
            formatted_date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            try:
                formatted_date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                try:
                    formatted_date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    try:
                        formatted_date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
                    except ValueError:
                        unmatched_keys_list.append(("------------------\nKey: " + str(key),
                                                    date_type + " Date Not Correct Format:",
                                                    "Expected Formats: %Y-%m-%dT%H:%M:%S",
                                                    "                  %Y-%m-%dT%H:%M:%SZ",
                                                    "                  %Y-%m-%dT%H:%M:%S.%f",
                                                    "                  %Y-%m-%dT%H:%M:%S.%fZ",
                                                    "Date: " + str(date_string)))

    else:
        try:
            formatted_date = datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            unmatched_keys_list.append(("------------------\nKey: " + str(key),
                                        date_type + " Date Not Correct Format:",
                                        "Expected Format: " + date_format,
                                        "Date: " + str(date_string)))
    return formatted_date
