import datetime
import json
import warnings

from RequestsLibrary import RequestsLibrary, utils
from Zoomba import ZoombaError
from dateutil.parser import parse
from urllib3.exceptions import InsecureRequestWarning
from requests.packages import urllib3
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.dotdict import DotDict
from pandas import to_datetime

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

    def call_get_request(self, headers=None, endpoint=None, fullstring=None, cookies=None, timeout=None, **kwargs):
        """ Generate a GET Request. This Keyword is basically a wrapper for get_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice\n
            timeout: (float) Time in seconds for the api to respond\n
            **kwargs: See https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html#GET for options.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
            along with any query parameters.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib.create_session("getapi", endpoint, headers, cookies=cookies, timeout=timeout)
        resp = requests_lib.get_on_session("getapi", fullstring, timeout=timeout, expected_status='any', **kwargs)
        return _convert_resp_to_dict(resp)

    def call_post_request(self, headers=None, endpoint=None, fullstring=None, data=None, files=None, cookies=None,
                          timeout=None, **kwargs):
        """ Generate a POST Request. This Keyword is basically a wrapper for post_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            files: (json) A JSON object that sends in the body of the request to be used by the specific Web service.\n
            **kwargs: See https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html#GET for options.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("postapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.post_on_session("postapi", fullstring, data, files=files, timeout=timeout,
                                            expected_status='any', **kwargs)
        return _convert_resp_to_dict(resp)

    def call_delete_request(self, headers=None, endpoint=None, fullstring=None, cookies=None, timeout=None, **kwargs):
        """ Generate a DELETE Request. This Keyword is basically a wrapper for delete_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            **kwargs: See https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html#GET for options.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        requests_lib.create_session("deleteapi", endpoint, headers, cookies=cookies, timeout=timeout)
        resp = requests_lib.delete_on_session("deleteapi", fullstring, timeout=timeout, expected_status='any', **kwargs)
        return _convert_resp_to_dict(resp)

    def call_patch_request(self, headers=None, endpoint=None, fullstring=None, data=None, cookies=None, timeout=None,
                           **kwargs):
        """ Generate a PATCH Request. This Keyword is basically a wrapper for patch_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            **kwargs: See https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html#GET for options.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("patchapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.patch_on_session("patchapi", fullstring, data, timeout=timeout, expected_status='any',
                                             **kwargs)
        return _convert_resp_to_dict(resp)

    def call_put_request(self, headers=None, endpoint=None, fullstring=None, data=None, cookies=None, timeout=None,
                         **kwargs):
        """ Generate a PUT Request. This Keyword is basically a wrapper for put_request from the RequestsLibrary.\n
            headers: (dictionary) The headers to be sent as part of the request.\n
            endpoint: (string) The string that identifies the url endpoint of the App that receives API requests.\n
            fullstring: (string) A string that contains the rest of the url that identifies a specific API/Webservice
            along with any query parameters.\n
            timeout: (float) Time in seconds for the api to respond\n
            data: (json) The JSON object to be sent on the body of the request to be used by the specific Web service.\n
            **kwargs: See https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html#GET for options.\n
            return: (response object) Returns the request response object, which includes headers, content, etc.
        """
        if self.suppress_warnings:
            urllib3.disable_warnings(InsecureRequestWarning)
        session = requests_lib.create_session("putapi", endpoint, headers, cookies=cookies, timeout=timeout)
        data = utils.format_data_according_to_header(session, data, headers)
        resp = requests_lib.put_on_session("putapi", fullstring, data, timeout=timeout, expected_status='any', **kwargs)
        return _convert_resp_to_dict(resp)

    def validate_response_contains_expected_response(self, json_actual_response, expected_response_dict,
                                                     ignored_keys=None, full_list_validation=False, identity_key="id",
                                                     sort_lists=False, **kwargs):
        """ This is the most used method for validating Request responses from an API against a supplied
            expected response. It performs an object to object comparison between two json objects, and if that fails,
            a more in depth method is called to find the exact discrepancies between the values of the provided objects.
            Additionally, a list of keys to ignore on the comparison may be supplied, for keys' values to be ignored./n

            json_actual_response: (request response object) The response from an API.\n
            expected_response_dict: (json) The expected response, in json format.\n
            ignored_keys: (strings list) A list of strings of the keys to be ignored on the validation.\n
            full_list_validation: (bool) Check that the entire list matches the expected response, defaults to False.\n
            identity_key: (string) Key to match items to, defaults to 'id'.\n
            sort_lists: (bool) Sort lists before doing key by key validation, defaults to False.\n
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
                                      unmatched_keys_list, full_list_validation=full_list_validation,
                                      sort_lists=sort_lists, **kwargs)
            self.generate_unmatched_keys_error_message(unmatched_keys_list)
            return
        if isinstance(actual_response_dict, list) and actual_response_dict:
            if full_list_validation:
                return self.full_list_validation(actual_response_dict, expected_response_dict, unmatched_keys_list,
                                                 ignored_keys, sort_lists=sort_lists, **kwargs)
            for exp_item in expected_response_dict:
                for actual_item in actual_response_dict:
                    try:
                        if exp_item[identity_key] == actual_item[identity_key]:
                            self.key_by_key_validator(actual_item, exp_item, ignored_keys, unmatched_keys_list,
                                                      full_list_validation=full_list_validation, sort_lists=sort_lists,
                                                      **kwargs)
                            self.generate_unmatched_keys_error_message(unmatched_keys_list)
                            break
                        elif actual_response_dict[-1] == actual_item:
                            ZoombaError(error='Item was not within the response:\n' + str(exp_item)).fail()
                            return
                        else:
                            continue
                    except KeyError:
                        ZoombaError(KeyError=f"\"{identity_key}\" Key was not in the response").fail()
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
                    ZoombaError(error=f"The response does not contain the key '{expected_key}'").fail()
                    continue
                if actual_response_dict[expected_key] != expected_response[expected_key]:
                    ZoombaError(
                        error="The value for the key '" + expected_key + "' doesn't match the response:",
                        expected=expected_response[expected_key],
                        actual=actual_response_dict[expected_key]
                    ).fail()
            return
        for expected_key in key_list:
            if expected_key not in actual_response_dict[0]:
                ZoombaError(error=f"The response does not contain the key '{expected_key}'").fail()
                continue
            if actual_response_dict[0][expected_key] != expected_response[0][expected_key]:
                ZoombaError(
                    error="The value for the key '" + expected_key + "' doesn't match the response:",
                    expected=expected_response[0][expected_key],
                    actual=actual_response_dict[0][expected_key]
                ).fail()
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
            ZoombaError(
                error="Did not pass number or string value, function expects a number or string 'IGNORE'.").fail()
            return

        if isinstance(actual_response_dict, list):
            if len(actual_response_dict) != int(number_of_items):
                ZoombaError(
                    error=f"API is returning {str(len(actual_response_dict))} instead of the expected "
                          f"{str(number_of_items)} result(s).").fail()
        else:
            ZoombaError(error="The response is not a list:", actual_response=f"\n{actual_response_dict}").fail()

    def key_by_key_validator(self, actual_dictionary, expected_dictionary, ignored_keys=None, unmatched_keys_list=None,
                             parent_key=None, full_list_validation=False, sort_lists=False, **kwargs):
        """ This method is used to find and verify the value of every key in the expectedItem dictionary when compared
            against a single dictionary actual_item, unless any keys are included on the ignored_keys array./n

            actual_item: (array of dictionaries) The list of dictionary items extracted from a json Response.\n
            ExpectedItem: (dictionary) The expected item with the key to be validated.\n
            ignored_keys: (strings list) A list of strings of the keys to be ignored on the validation.\n
            full_list_validation: (bool) Check that the entire list matches the expected response, defaults to False.\n
            sort_lists: (bool) Sort lists before doing key by key validation, defaults to False.\n
            **kwargs: (dict) Currently supported kwargs are margin_type and margin_amt\n
            margin_type: (string) The type of unit of time to be used to generate a delta for the date comparisons.\n
            margin_amt: (string/#) The amount of units specified in margin_type to allot for difference between dates.\n
            return: (boolean) If the method completes successfully, it returns True. Appropriate error messages are
            returned otherwise.\n
        """
        if len(actual_dictionary) != len(expected_dictionary):
            ZoombaError(
                error="Collections not the same length:",
                actual_length=str(len(actual_dictionary)),
                expected_length=str(len(expected_dictionary))).fail()
            return
        for key, value in expected_dictionary.items():
            if ignored_keys and key in ignored_keys:
                continue
            if key not in actual_dictionary:
                ZoombaError(
                    error="Key not found in Actual",
                    actual=actual_dictionary,
                    key=key
                ).fail()
                continue
            if isinstance(value, list):
                if full_list_validation and len(value) != len(actual_dictionary[key]):
                    ZoombaError(
                        error="Arrays not the same length",
                        expected=value,
                        actual=actual_dictionary[key]
                    ).fail()
                    continue
                self._key_by_key_list(key, value, actual_dictionary, unmatched_keys_list, ignored_keys, parent_key,
                                      full_list_validation=full_list_validation, sort_lists=sort_lists, **kwargs)
            elif isinstance(value, dict):
                self._key_by_key_dict(key, value, actual_dictionary, expected_dictionary, unmatched_keys_list,
                                      ignored_keys, full_list_validation=full_list_validation, sort_lists=sort_lists,
                                      **kwargs)
            elif (isinstance(expected_dictionary[key], str) and not expected_dictionary[key].isdigit()) or isinstance(
                    expected_dictionary[key], datetime.datetime):
                try:
                    if not isinstance(expected_dictionary[key], datetime.datetime):
                        parse(expected_dictionary[key])
                    self.date_string_comparator(value, actual_dictionary[key], key, unmatched_keys_list, **kwargs)
                except (ValueError, TypeError):
                    if value == actual_dictionary[key]:
                        continue
                    else:
                        unmatched_keys_list.append(ZoombaError(key=key, expected=value, actual=actual_dictionary[key]))
            elif value == actual_dictionary[key]:
                continue
            else:
                unmatched_keys_list.append(ZoombaError(key=key, expected=value, actual=actual_dictionary[key]))
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
        unmatched_keys_list.append(
            ZoombaError(
                note="Dates Not Close Enough",
                key=key,
                expected=expected_date,
                actual=actual_date))

    def generate_unmatched_keys_error_message(self, unmatched_keys):
        """ This method is only used as an internal call from other validating methods to generate an error string
            containing every unmatched key when a validation fails.\n
            unmatchedKeys: (array of key/value pairs) An array containing the unmatched keys during a validation.\n
        """
        if unmatched_keys:
            ZoombaError(
                error="Key(s) Did Not Match",
                unmatched_keys_list="\n" + "\n".join([str(key) for key in unmatched_keys]),
                note="Please see differing value(s)"
            ).fail()

    def _key_by_key_list(self, key, value, actual_dictionary, unmatched_keys_list=None, ignored_keys=None,
                         parent_key=None, full_list_validation=False, sort_lists=False, **kwargs):
        if sort_lists and isinstance(value, list):
            try:
                value = list(map(dict, sorted(list(i.items()) for i in value)))
            except AttributeError:
                pass
        for index, item in enumerate(value):
            if isinstance(item, str):
                if value != actual_dictionary[key]:
                    if sort_lists:
                        sorted_value = sorted(value)
                        sorted_actual = sorted(actual_dictionary[key])
                        if sorted_value != sorted_actual:
                            ZoombaError(
                                error="Arrays do not match",
                                expected=sorted_value,
                                actual=sorted_actual
                            ).fail()
                            continue
                    else:
                        ZoombaError(
                            error="Arrays do not match",
                            expected=value,
                            actual=actual_dictionary[key],
                            tip="If this is simply out of order try 'sort_list=True'"
                        ).fail()
                        continue
            else:
                if len(actual_dictionary[key]) == 0:
                    actual_item = ''
                else:
                    if sort_lists:
                        actual_dictionary[key] = list(
                            map(dict, sorted(list(i.items()) for i in actual_dictionary[key])))
                    actual_item = actual_dictionary[key][index]
                temp_actual_dict = {key: actual_item}
                temp_expected_dict = {key: item}
                if unmatched_keys_list:
                    current_unmatched_length = len(unmatched_keys_list)
                else:
                    current_unmatched_length = 0
                self.key_by_key_validator(temp_actual_dict, temp_expected_dict,
                                          ignored_keys, unmatched_keys_list, parent_key=key,
                                          full_list_validation=full_list_validation, sort_lists=sort_lists, **kwargs)
                if unmatched_keys_list is None:
                    continue
                else:
                    _unmatched_list_check(unmatched_keys_list, current_unmatched_length,
                                          key, index, parent_key, is_list=True)

    def _key_by_key_dict(self, key, value, actual_dictionary, expected_dictionary, unmatched_keys_list=None,
                         ignored_keys=None, full_list_validation=False, sort_lists=False, **kwargs):
        try:
            if len(value) != len(actual_dictionary[key]):
                ZoombaError(
                    error="Dicts do not match",
                    expected=value,
                    actual=actual_dictionary[key]
                ).fail()
                return
        except TypeError:
            ZoombaError(
                error="Dicts do not match",
                expected=value,
                actual="Actual is not a valid dictionary."
            ).fail()
            return
        if unmatched_keys_list is not None:
            current_unmatched_length = len(unmatched_keys_list)
        self.key_by_key_validator(actual_dictionary[key], expected_dictionary[key],
                                  ignored_keys, unmatched_keys_list, parent_key=key,
                                  full_list_validation=full_list_validation, sort_lists=sort_lists, **kwargs)
        if unmatched_keys_list is None:
            return
        _unmatched_list_check(unmatched_keys_list, current_unmatched_length, key)

    def full_list_validation(self, actual_response_dict, expected_response_dict, unmatched_keys_list, ignored_keys=None,
                             sort_lists=False, **kwargs):
        if actual_response_dict == expected_response_dict:
            return
        for actual_item, expected_item in zip(actual_response_dict, expected_response_dict):
            self.key_by_key_validator(actual_item, expected_item, ignored_keys, unmatched_keys_list,
                                      full_list_validation=True, sort_lists=sort_lists, **kwargs)
        if unmatched_keys_list:
            unmatched_keys_list.append(ZoombaError(
                full_list_breakdown=f"\n{ZoombaError(expected=expected_response_dict, actual=actual_response_dict)}",
                important="full_list_breakdown"
            ))
            self.generate_unmatched_keys_error_message(unmatched_keys_list)
        return


def _unmatched_list_check(unmatched_keys_list, current_unmatched_length, key, index=None, parent_key=None,
                          is_list=False):
    if len(unmatched_keys_list) <= current_unmatched_length:
        return
    adjusted_list_items = []

    for new_index in range(len(unmatched_keys_list) - current_unmatched_length):
        unmatched_zoomba_error = unmatched_keys_list.pop()
        if parent_key == key:
            remnant = unmatched_zoomba_error.key.replace(parent_key, "", 1)
            unmatched_zoomba_error.key = f"{parent_key}[{index}]{remnant}"

        elif parent_key is not None:
            if not unmatched_zoomba_error.key.startswith(key):
                remnant = unmatched_zoomba_error.key
                if is_list:
                    unmatched_zoomba_error.key = f"{key}[{index}].{remnant}"
                else:
                    unmatched_zoomba_error.key = f"{key}.{remnant}"

        elif is_list:
            remnant = unmatched_zoomba_error.key.replace(f"{key}[{index}]", "", 1)
            if f"{key}[{index}]" not in unmatched_zoomba_error.key:
                if key == remnant:
                    unmatched_zoomba_error.key = f"{key}[{index}]"
                else:
                    unmatched_zoomba_error.key = f"{key}[{index}].{remnant}"
        adjusted_list_items.append(unmatched_zoomba_error)

    unmatched_keys_list.extend(adjusted_list_items)


def _date_format(date_string, key, unmatched_keys_list, date_type, date_format=None):
    formatted_date = None
    warnings.filterwarnings("ignore", message=".*Discarding nonzero nanoseconds in conversion.*")
    if (date_format is None) and (date_string is not None):
        try:
            formatted_date = to_datetime(date_string).tz_localize(None).to_pydatetime()
        except ValueError:
            unmatched_keys_list.append(
                ZoombaError(
                    key=key,
                    note=f"{date_type} Date Not Correct Format",
                    expected_formats="%Y-%m-%dT%H:%M:%S\n" +
                                     "                  %Y-%m-%dT%H:%M:%SZ\n" +
                                     "                  %Y-%m-%dT%H:%M:%S.%f\n" +
                                     "                  %Y-%m-%dT%H:%M:%S.%fZ",
                    date=date_string))
    else:
        try:
            formatted_date = datetime.datetime.strptime(date_string, date_format)
        except ValueError:
            unmatched_keys_list.append(
                ZoombaError(
                    key=key,
                    note=f"{date_type} Date Not Correct Format",
                    expected_format=date_format,
                    date=date_string))
    return formatted_date


def _convert_resp_to_dict(response):
    new_response = {
        item: getattr(response, item)
        for item in dir(response)
        if item[0] != '_'
    }

    return DotDict(new_response)
