import datetime
import json

from RequestsLibrary import RequestsLibrary, utils
from dateutil.parser import parse
from urllib3.exceptions import InsecureRequestWarning
from requests.packages import urllib3
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.dotdict import DotDict

zoomba = BuiltIn()
requests_lib = RequestsLibrary()


class APILibrary:
    """Zoomba API Library

        This class is the base Library used to generate automated API Tests in the Robot Automation Framework.
        It has been generated to accommodate the RESTful API design pattern.
    """
    def __init__(self):
        self.suppress_warnings = False

    def suppress_insecure_request_warnings(self, suppress="True"):
        """Suppress Insecure Request Warnings. This keyword suppresses or un-suppresses insecure request warnings\n
        suppress: (bool) True/False to suppress warnings, default is True\n
        Examples:
        | Suppress Insecure Request Warnings                       #Suppresses Insecure Request Warnings
        | Suppress Insecure Request Warnings | suppress=True |     #Suppresses Insecure Request Warnings
        | Suppress Insecure Request Warnings | False |    #Does Not Suppresses Insecure Request Warnings
        """
        self.suppress_warnings = "FALSE" not in suppress.upper()

    def call_get_request(self, headers=None, endpoint=None, fullstring=None, cookies=None, timeout=None):
        """ Generate a GET Request. This Keyword is basically a wrapper for get_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice\n
            timeout: (float) Time in seconds for the api to respond\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
            along with any query parameters.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib.create_session("getapi", endpoint, headers, cookies=cookies, timeout=timeout)
        resp = requests_lib.get_on_session("getapi", fullstring, timeout=timeout, expected_status='any')
        return _convert_resp_to_dict(resp)

    def call_post_request(self, headers=None, endpoint=None, fullstring=None, data=None, files=None, cookies=None, timeout=None):
        """ Generate a POST Request. This Keyword is basically a wrapper for post_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            files: (json) A JSON object that sends in the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("postapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.post_on_session("postapi", fullstring, data, files=files, timeout=timeout, expected_status='any')
        return _convert_resp_to_dict(resp)

    def call_delete_request(self, headers=None, endpoint=None, fullstring=None, cookies=None, timeout=None):
        """ Generate a DELETE Request. This Keyword is basically a wrapper for delete_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib.create_session("deleteapi", endpoint, headers, cookies=cookies, timeout=timeout)
        resp = requests_lib.delete_on_session("deleteapi", fullstring, timeout=timeout, expected_status='any')
        return _convert_resp_to_dict(resp)

    def call_patch_request(self, headers=None, endpoint=None, fullstring=None, data=None, cookies=None, timeout=None):
        """ Generate a PATCH Request. This Keyword is basically a wrapper for patch_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("patchapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.patch_on_session("patchapi", fullstring, data, timeout=timeout, expected_status='any')
        return _convert_resp_to_dict(resp)

    def call_put_request(self, headers=None, endpoint=None, fullstring=None, data=None, cookies=None, timeout=None):
        """ Generate a PUT Request. This Keyword is basically a wrapper for put_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("putapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.put_on_session("putapi", fullstring, data, timeout=timeout, expected_status='any')
        return _convert_resp_to_dict(resp)

    def create_connection(self, endpoint, method, data, headers=None, cookies=None, timeout=None):
        """*DEPRECATED!!* Use 'Call Post Request' instead."""
        return self.call_post_request(headers=headers, endpoint=endpoint, fullstring=method, data=data, cookies=cookies, timeout=timeout)

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
            zoomba.fail("The Actual Response is Empty.")
            return
        actual_response_dict = json.loads(json_actual_response)
        unmatched_keys_list = []
        if not isinstance(actual_response_dict, list) and actual_response_dict:
            if actual_response_dict == expected_response_dict:
                return
            self.key_by_key_validator(actual_response_dict, expected_response_dict, ignored_keys,
                                      unmatched_keys_list, full_list_validation=full_list_validation, **kwargs)
            self.generate_unmatched_keys_error_message(unmatched_keys_list)
            return
        if isinstance(actual_response_dict, list) and actual_response_dict:
            if full_list_validation:
                return self.full_list_validation(actual_response_dict, expected_response_dict, unmatched_keys_list,
                                                 ignored_keys, **kwargs)
            for exp_item in expected_response_dict:
                for actual_item in actual_response_dict:
                    try:
                        if exp_item[identity_key] == actual_item[identity_key]:
                            self.key_by_key_validator(actual_item, exp_item, ignored_keys, unmatched_keys_list,
                                                      full_list_validation=full_list_validation, **kwargs)
                            self.generate_unmatched_keys_error_message(unmatched_keys_list)
                            break
                        elif actual_response_dict[-1] == actual_item:
                            zoomba.fail('Item was not within the response:\n' + str(exp_item))
                            return
                        else:
                            continue
                    except KeyError:
                        zoomba.fail('KeyError: "' + identity_key + '" Key was not in the response')
                        break
        else:
            zoomba.fail("The Actual Response is Empty.")

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
        if not isinstance(actual_response_dict, list):
            for expected_key in key_list:
                if expected_key not in actual_response_dict:
                    zoomba.fail("The response does not contain the key '" + expected_key + "'")
                    continue
                if actual_response_dict[expected_key] != expected_response[expected_key]:
                    zoomba.fail("The value for the key '" + expected_key + "' doesn't match the response:" + \
                                "\nExpected: " + expected_response[expected_key] +\
                                "\nActual: " + actual_response_dict[expected_key])
            return
        for expected_key in key_list:
            if expected_key not in actual_response_dict[0]:
                zoomba.fail("The response does not contain the key '" + expected_key + "'")
                continue
            if actual_response_dict[0][expected_key] != expected_response[0][expected_key]:
                zoomba.fail("The value for the key '" + expected_key + "' doesn't match the response:" + \
                            "\nExpected: " + expected_response[0][expected_key] + \
                            "\nActual: " + actual_response_dict[0][expected_key])
        return

    def validate_response_contains_correct_number_of_items(self, json_actual_response, number_of_items):
        """ This keyword is used to validate the number of returned items on Request responses from an API.\n
            json_actual_response: (request response object) The response from an API.\n
            number_of_items: (integer) The expected number of items.\n
            return: There is no actual returned output, other than error messages when comparisons fail.\n
        """
        actual_response_dict = json.loads(json_actual_response)
        if isinstance(number_of_items, str):
            number_of_items = number_of_items.upper()
            if number_of_items == "IGNORE":
                return True
        elif not isinstance(number_of_items, int):
            zoomba.fail("Did not pass number or string value, function expects a number or string 'IGNORE'.")
            return

        if isinstance(actual_response_dict, list):
            if len(actual_response_dict) != number_of_items:
                zoomba.fail('API is returning ' + str(
                    len(actual_response_dict)) + ' instead of the expected ' + str(number_of_items) + ' result(s).')
        else:
            zoomba.fail("The response is not a list:\nActual Response:\n" + str(actual_response_dict))

    def key_by_key_validator(self, actual_dictionary, expected_dictionary, ignored_keys=None, unmatched_keys_list=None,
                             parent_key=None, full_list_validation=False, **kwargs):
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
        if len(actual_dictionary) != len(expected_dictionary):
            zoomba.fail("Collections not the same length:"\
                        "\nActual length: " + str(len(actual_dictionary)) +\
                        "\nExpected length " + str(len(expected_dictionary)))
            return
        for key, value in expected_dictionary.items():
            if ignored_keys and key in ignored_keys:
                continue
            if key not in actual_dictionary:
                zoomba.fail("Key not found in Actual : " + str(actual_dictionary) + " Key: " + str(key))
                continue
            if isinstance(value, list):
                if full_list_validation and len(value) != len(actual_dictionary[key]):
                    zoomba.fail("Arrays not the same length:" + \
                                "\nExpected: " + str(value) + \
                                "\nActual: " + str(actual_dictionary[key]))
                    continue
                self._key_by_key_list(key, value, actual_dictionary, unmatched_keys_list, ignored_keys, parent_key,
                                      full_list_validation=full_list_validation, **kwargs)
            elif isinstance(value, dict):
                self._key_by_key_dict(key, value, actual_dictionary, expected_dictionary, unmatched_keys_list,
                                      ignored_keys, full_list_validation=full_list_validation, **kwargs)
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
        expected_utc = _date_format(expected_date, key, unmatched_keys_list, "Expected")
        actual_utc = _date_format(actual_date, key, unmatched_keys_list, "Actual")
        if expected_utc and actual_utc:
            self.date_comparator(expected_utc, actual_utc, key, unmatched_keys_list, **kwargs)

    def date_comparator(self, expected_date, actual_date, key, unmatched_keys_list, margin_type="minutes",
                        margin_amt=10):
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
        if expected_date - margin <= actual_date <= expected_date + margin:
            return
        unmatched_keys_list.append(("------------------\n" + "Dates Not Close Enough\nKey: " + str(key),
                                    "Expected: " + str(expected_date),
                                    "Actual: " + str(actual_date)))

    def generate_unmatched_keys_error_message(self, unmatched_keys):
        """ This method is only used as an internal call from other validating methods to generate an error string
            containing every unmatched key when a validation fails.\n
            unmatchedKeys: (array of key/value pairs) An array containing the unmatched keys during a validation.\n
        """
        if unmatched_keys:
            keys_error_msg = "Key(s) Did Not Match:\n"
            for key_error_tuple in unmatched_keys:
                for key_error in key_error_tuple:
                    keys_error_msg += str(key_error) + "\n"
            zoomba.fail(keys_error_msg + "\nPlease see differing value(s)")

    def _key_by_key_list(self, key, value, actual_dictionary, unmatched_keys_list=None, ignored_keys=None,
                         parent_key=None, full_list_validation=False, **kwargs):
        for index, item in enumerate(value):
            if isinstance(item, str):
                if value != actual_dictionary[key]:
                    zoomba.fail("Arrays do not match:" + \
                                "\nExpected: " + str(value) + \
                                "\nActual: " + str(actual_dictionary[key]))
                    continue
            else:
                if len(actual_dictionary[key]) == 0:
                    actual_item = ''
                else:
                    actual_item = actual_dictionary[key][index]
                temp_actual_dict = {key: actual_item}
                temp_expected_dict = {key: item}
                if unmatched_keys_list:
                    current_unmatched_length = len(unmatched_keys_list)
                else:
                    current_unmatched_length = 0
                self.key_by_key_validator(temp_actual_dict, temp_expected_dict,
                                          ignored_keys, unmatched_keys_list, parent_key=key,
                                          full_list_validation=full_list_validation, **kwargs)
                if unmatched_keys_list is None:
                    continue
                else:
                    _unmatched_list_check(unmatched_keys_list, current_unmatched_length,
                                          key, index, parent_key, is_list=True)

    def _key_by_key_dict(self, key, value, actual_dictionary, expected_dictionary, unmatched_keys_list=None,
                         ignored_keys=None, full_list_validation=False, **kwargs):
        try:
            if len(value) != len(actual_dictionary[key]):
                zoomba.fail("Dicts do not match:" + \
                            "\nExpected: " + str(value) + \
                            "\nActual: " + str(actual_dictionary[key]))
                return
        except TypeError:
            zoomba.fail("Dicts do not match:" + \
                        "\nExpected: " + str(value) + \
                        "\nActual is not a valid dictionary.")
            return
        if unmatched_keys_list is not None:
            current_unmatched_length = len(unmatched_keys_list)
        self.key_by_key_validator(actual_dictionary[key], expected_dictionary[key],
                                  ignored_keys, unmatched_keys_list, parent_key=key,
                                  full_list_validation=full_list_validation, **kwargs)
        if unmatched_keys_list is None:
            return
        _unmatched_list_check(unmatched_keys_list, current_unmatched_length, key)

    def full_list_validation(self, actual_response_dict, expected_response_dict, unmatched_keys_list, ignored_keys=None,
                             **kwargs):
        if actual_response_dict == expected_response_dict:
            return
        for actual_item, expected_item in zip(actual_response_dict, expected_response_dict):
            self.key_by_key_validator(actual_item, expected_item, ignored_keys, unmatched_keys_list,
                                      full_list_validation=True, **kwargs)
        if unmatched_keys_list:
            unmatched_keys_list.append(("------------------\n" + "Full List Breakdown:",
                                        "Expected: " + str(expected_response_dict),
                                        "Actual: " + str(actual_response_dict)))
            self.generate_unmatched_keys_error_message(unmatched_keys_list)
        return


def _unmatched_list_check(unmatched_keys_list, current_unmatched_length, key, index=None, parent_key=None,
                          is_list=False):
    if len(unmatched_keys_list) > current_unmatched_length and parent_key == key:
        for new_index in range(len(unmatched_keys_list) - current_unmatched_length):
            reverse_index = -1 * (new_index + 1)
            unmatched_tuple = unmatched_keys_list[reverse_index]
            split_key_string = unmatched_tuple[0].split("Key: " + parent_key)
            new_key_string = split_key_string[0] + "Key: " + parent_key + "[" + str(index) + "]" + split_key_string[1]
            unmatched_keys_list[reverse_index] = (new_key_string, *unmatched_tuple[1:])
    elif len(unmatched_keys_list) > current_unmatched_length and parent_key is not None:
        for new_index in range(len(unmatched_keys_list) - current_unmatched_length):
            reverse_index = -1 * (new_index + 1)
            unmatched_tuple = unmatched_keys_list[reverse_index]
            if "Key: " + str(key) not in unmatched_tuple[0]:
                split_key_string = unmatched_tuple[0].split("Key: ")
                if is_list:
                    new_key_string = split_key_string[0] + "Key: " + key + "[" + str(index) + "]." + split_key_string[1]
                else:
                    new_key_string = split_key_string[0] + "Key: " + key + "." + split_key_string[1]
                unmatched_keys_list[reverse_index] = (new_key_string, *unmatched_tuple[1:])
    elif len(unmatched_keys_list) > current_unmatched_length and is_list:
        for new_index in range(len(unmatched_keys_list) - current_unmatched_length):
            reverse_index = -1 * (new_index + 1)
            unmatched_tuple = unmatched_keys_list[reverse_index]
            if str(key) + "[" + str(index) + "]" not in unmatched_tuple[0]:
                split_key_string = unmatched_tuple[0].split("Key: ")
                if key == split_key_string[1]:
                    new_key_string = split_key_string[0] + "Key: " + key + "[" + str(index) + "]"
                else:
                    new_key_string = split_key_string[0] + "Key: " + key + "[" + str(index) + "]" + \
                                     "." + split_key_string[1]
                unmatched_keys_list[reverse_index] = (new_key_string, *unmatched_tuple[1:])


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
                        try:
                            formatted_date = parse(date_string, fuzzy=True)
                            formatted_date = str(formatted_date).replace('+00:00', 'Z')
                            formatted_date = formatted_date.replace(' ', 'T')
                            formatted_date = datetime.datetime.strptime(formatted_date, "%Y-%m-%dT%H:%M:%S.%fZ")
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


def _convert_resp_to_dict(response):
    new_response = {
        item: getattr(response, item)
        for item in dir(response)
        if item[0] != '_'
    }

    return DotDict(new_response)
