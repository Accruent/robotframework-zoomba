import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/')))
import unittest
from Zoomba.APILibrary import APILibrary
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestInternal(unittest.TestCase):
    def test_suppress_default(self):
        library = APILibrary()
        assert not library.suppress_warnings

    def test_suppress_set(self):
        library = APILibrary()
        library.suppress_insecure_request_warnings("True")
        assert library.suppress_warnings

    def test_suppress_set_default(self):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        assert library.suppress_warnings

    def test_suppress_set_false(self):
        library = APILibrary()
        library.suppress_warnings = True
        library.suppress_insecure_request_warnings("False")
        assert not library.suppress_warnings


class TestExternal(unittest.TestCase):
    def test_get_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_get_request)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    def test_basic_get(self, create_session, get_request):
        library = APILibrary()
        r = library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with("getapi", "fullstring", timeout=None)
        get_request.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    def test_get_called_with(self, get_request, create_session):
        library = APILibrary()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        get_request.assert_called_with("getapi", "fullstring", timeout=None)
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_get_insecure_request(self, disable_warnings, get_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        get_request.assert_called_with("getapi", "fullstring", timeout=None)
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    def test_get_with_cookies(self, get_request, create_session):
        library = APILibrary()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring", "chocolate_chip")
        assert get_request.called_with("getapi", "fullstring")
        assert create_session.called_with("getapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip")

    def test_post_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_post_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_basic_post(self, post_on_session, create_session):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        post_on_session.assert_called_with('postapi', 'fullstring', None, files=None, timeout=None,
                                          expected_status='any')
        create_session.assert_called_with("postapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_files_post(self, post_on_session, create_session):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring", b'item')
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        post_on_session.assert_called_with('postapi', 'fullstring', b'item', files=None, timeout=None,
                                          expected_status='any')
        create_session.assert_called_with("postapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_post_insecure_request(self, disable_warnings, post_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        post_on_session.assert_called_with('postapi', 'fullstring', None, files=None, timeout=None,
                                           expected_status='any')
        create_session.assert_called_with("postapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_post_with_cookies(self, post_on_session, create_session):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        type(r).cookies = PropertyMock(return_value={"chocolate_chip": "tasty"})
        assert r.text == "success"
        assert r.status_code == 200
        assert r.cookies["chocolate_chip"] == "tasty"
        post_on_session.assert_called_with('postapi', 'fullstring', None, files='chocolate_chip', timeout=None,
                                           expected_status='any')
        create_session.assert_called_with("postapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    def test_delete_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_delete_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.delete_on_session')
    def test_basic_delete(self, create_session, delete_on_session):
        library = APILibrary()
        r = library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        delete_on_session.assert_called_with('deleteapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        create_session.assert_called_with('deleteapi', 'fullstring', timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.delete_on_session')
    def test_delete_called_with(self, delete_on_session, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        delete_on_session.assert_called_with("deleteapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.delete_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_delete_insecure_request(self, disable_warnings, delete_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        create_session.assert_called_with('deleteapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        delete_on_session.assert_called_with('deleteapi', 'fullstring', timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.delete_on_session')
    def test_delete_with_cookies(self, delete_on_session, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        delete_on_session.assert_called_with("deleteapi", "fullstring", timeout='chocolate_chip', expected_status='any')
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies=None, timeout='chocolate_chip')

    def test_patch_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_patch_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.patch_on_session')
    def test_basic_patch(self, patch_on_session, create_session):
        library = APILibrary()
        r = library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('patchapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        patch_on_session.assert_called_with('patchapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.patch_on_session')
    def test_patch_called_with(self, patch_on_session, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.patch_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_patch_insecure_request(self, disable_warnings, patch_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.patch_on_session')
    def test_patch_with_cookies(self, patch_on_session, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip", timeout=None)

    def test_put_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_put_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.put_on_session')
    def test_basic_put(self, put_on_session, create_session):
        library = APILibrary()
        r = library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('putapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        put_on_session.assert_called_with('putapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.put_on_session')
    def test_put_called_with(self, put_on_session, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        put_on_session.assert_called_with("putapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.put_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_put_insecure_request(self, disable_warnings, put_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        create_session.assert_called_with('putapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        put_on_session.assert_called_with('putapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.put_on_session')
    def test_put_with_cookies(self, put_on_session, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        put_on_session.assert_called_with("putapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip", timeout=None)

    def test_create_connection_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.create_connection)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_basic_create_connection(self, post_on_session, create_session):
        library = APILibrary()
        r = library.create_connection("Endpoint", "fullstring", None, headers={"a": "Text"})
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('postapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        post_on_session.assert_called_with('postapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_files_create_connection(self, post_on_session, create_session):
        library = APILibrary()
        r = library.create_connection("Endpoint", "fullstring", b'item', headers={"a": "Text"})
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('postapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        post_on_session.assert_called_with('postapi', 'fullstring', b'item', timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_create_connection_insecure_request(self, disable_warnings, post_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.create_connection("Endpoint", "fullstring", None, headers={"a": "Text"})
        disable_warnings.assert_called()
        create_session.assert_called_with('postapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        post_on_session.assert_called_with('postapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch('RequestsLibrary.RequestsOnSessionKeywords.post_on_session')
    def test_create_connection_with_cookies(self, post_on_session, create_session):
        library = APILibrary()
        r = library.create_connection("Endpoint", "fullstring", None, {"a": "Text"}, "chocolate_chip")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        type(r).cookies = PropertyMock(return_value={"chocolate_chip": "tasty"})
        assert r.text == "success"
        assert r.status_code == 200
        assert r.cookies["chocolate_chip"] == "tasty"
        create_session.assert_called_with('postapi', 'Endpoint', {'a': 'Text'}, cookies='chocolate_chip', timeout=None)
        post_on_session.assert_called_with('postapi', 'fullstring', None, timeout=None, expected_status='any')
