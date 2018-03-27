import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.APILibrary import APILibrary
import unittest
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

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    def test_get_called_with(self, get_request, create_session):
        library = APILibrary()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        get_request.assert_called_with("getapi", "fullstring")
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_get_insecure_request(self, disable_warnings, get_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

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

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_basic_post(self, create_session, post_request):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_files_post(self, create_session, post_request):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring", b'item')
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_post_insecure_request(self, disable_warnings, post_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_post_with_cookies(self, post_request, create_session):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        type(r).cookies = PropertyMock(return_value={"chocolate_chip": "tasty"})
        assert r.text == "success"
        assert r.status_code == 200
        assert r.cookies["chocolate_chip"] == "tasty"

    def test_delete_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_delete_request)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.delete_request')
    def test_basic_delete(self, create_session, delete_request):
        library = APILibrary()
        r = library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.delete_request')
    def test_delete_called_with(self, delete_request, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        delete_request.assert_called_with("deleteapi", "fullstring", None)
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.delete_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_delete_insecure_request(self, disable_warnings, delete_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.delete_request')
    def test_delete_with_cookies(self, delete_request, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        delete_request.assert_called_with("deleteapi", "fullstring", None)
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip")

    def test_patch_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_patch_request)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.patch_request')
    def test_basic_patch(self, create_session, patch_request):
        library = APILibrary()
        r = library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.patch_request')
    def test_patch_called_with(self, patch_request, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        patch_request.assert_called_with("patchapi", "fullstring", None)
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.patch_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_patch_insecure_request(self, disable_warnings, patch_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.patch_request')
    def test_patch_with_cookies(self, patch_request, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        patch_request.assert_called_with("patchapi", "fullstring", None)
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip")

    def test_put_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_put_request)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.put_request')
    def test_basic_put(self, create_session, put_request):
        library = APILibrary()
        r = library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.put_request')
    def test_put_called_with(self, put_request, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        put_request.assert_called_with("putapi", "fullstring", None)
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies=None)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.put_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_put_insecure_request(self, disable_warnings, put_request, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.put_request')
    def test_put_with_cookies(self, put_request, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        put_request.assert_called_with("putapi", "fullstring", None)
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip")

    def test_create_connection_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.create_connection)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_basic_create_connection(self, create_session, post_request):
        library = APILibrary()
        r = library.create_connection({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_files_create_connection(self, create_session, post_request):
        library = APILibrary()
        r = library.create_connection({"a": "Text"}, "Endpoint", "fullstring", b'item')
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_create_connection_insecure_request(self, disable_warnings, create_session, post_request):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.create_connection({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_create_connection_with_cookies(self, create_session, post_request):
        library = APILibrary()
        r = library.create_connection({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        type(r).cookies = PropertyMock(return_value={"chocolate_chip": "tasty"})
        assert r.text == "success"
        assert r.status_code == 200
        assert r.cookies["chocolate_chip"] == "tasty"
