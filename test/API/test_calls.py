import os
import sys

import RequestsLibrary.SessionKeywords

sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/')))
from Zoomba.APILibrary import APILibrary
from unittest.mock import patch, PropertyMock
from unittest import TestCase

# Python 3.11 seems to treat the patch statement here differently
if sys.version_info[:3] > (3, 10):
    requestsSessionKeywords = 'RequestsLibrary.RequestsOnSessionKeywords.RequestsOnSessionKeywords'
else:
    requestsSessionKeywords = 'RequestsLibrary.RequestsOnSessionKeywords'


class TestInternal(TestCase):
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


class TestExternal(TestCase):
    def test_get_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_get_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.get_on_session')
    def test_basic_get(self, get_on_session, create_session):
        library = APILibrary()
        r = library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        get_on_session.assert_called_with("getapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.get_on_session')
    def test_get_called_with(self, get_on_session, create_session):
        library = APILibrary()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        get_on_session.assert_called_with("getapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.get_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_get_insecure_request(self, disable_warnings, get_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        get_on_session.assert_called_with("getapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.get_on_session')
    def test_get_with_cookies(self, get_on_session, create_session):
        library = APILibrary()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring", "chocolate_chip")
        get_on_session.assert_called_with("getapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip", timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.get_on_session')
    def test_get_with_kwarg(self, get_on_session, create_session):
        library = APILibrary()
        r = library.call_get_request({"a": "Text"}, "Endpoint", "fullstring", allow_redirects=False)
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        get_on_session.assert_called_with("getapi", "fullstring", timeout=None, expected_status='any',
                                          allow_redirects=False)
        create_session.assert_called_with("getapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    def test_post_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_post_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.post_on_session')
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
    @patch(f'{requestsSessionKeywords}.post_on_session')
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
    @patch(f'{requestsSessionKeywords}.post_on_session')
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
    @patch(f'{requestsSessionKeywords}.post_on_session')
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

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.post_on_session')
    def test_post_with_kwarg(self, post_on_session, create_session):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring", allow_redirects=False)
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        post_on_session.assert_called_with('postapi', 'fullstring', None, files=None, timeout=None,
                                           expected_status='any', allow_redirects=False)
        create_session.assert_called_with("postapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    def test_delete_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_delete_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.delete_on_session')
    def test_basic_delete(self, delete_on_session, create_session):
        library = APILibrary()
        r = library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('deleteapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        delete_on_session.assert_called_with('deleteapi', 'fullstring', timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.delete_on_session')
    def test_delete_called_with(self, delete_on_session, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        delete_on_session.assert_called_with("deleteapi", "fullstring", timeout=None, expected_status='any')
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.delete_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_delete_insecure_request(self, disable_warnings, delete_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        create_session.assert_called_with('deleteapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        delete_on_session.assert_called_with('deleteapi', 'fullstring', timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.delete_on_session')
    def test_delete_with_cookies(self, delete_on_session, create_session):
        library = APILibrary()
        library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        delete_on_session.assert_called_with("deleteapi", "fullstring", timeout='chocolate_chip',
                                             expected_status='any')
        create_session.assert_called_with("deleteapi", "Endpoint", {"a": "Text"}, cookies=None,
                                          timeout='chocolate_chip')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.delete_on_session')
    def test_delete_with_kwarg(self, delete_on_session, create_session):
        library = APILibrary()
        r = library.call_delete_request({"a": "Text"}, "Endpoint", "fullstring", data="{test}")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('deleteapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        delete_on_session.assert_called_with('deleteapi', 'fullstring', timeout=None, expected_status='any',
                                             data="{test}")

    def test_patch_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_patch_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.patch_on_session')
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
    @patch(f'{requestsSessionKeywords}.patch_on_session')
    def test_patch_called_with(self, patch_on_session, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.patch_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_patch_insecure_request(self, disable_warnings, patch_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.patch_on_session')
    def test_patch_with_cookies(self, patch_on_session, create_session):
        library = APILibrary()
        library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        patch_on_session.assert_called_with("patchapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("patchapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip", timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.patch_on_session')
    def test_patch_with_kwarg(self, patch_on_session, create_session):
        library = APILibrary()
        r = library.call_patch_request({"a": "Text"}, "Endpoint", "fullstring", allow_redirects=False)
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('patchapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        patch_on_session.assert_called_with('patchapi', 'fullstring', None, timeout=None, expected_status='any',
                                            allow_redirects=False)

    def test_put_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_put_request)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.put_on_session')
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
    @patch(f'{requestsSessionKeywords}.put_on_session')
    def test_put_called_with(self, put_on_session, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        put_on_session.assert_called_with("putapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies=None, timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.put_on_session')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_put_insecure_request(self, disable_warnings, put_on_session, create_session):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring")
        disable_warnings.assert_called()
        create_session.assert_called_with('putapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        put_on_session.assert_called_with('putapi', 'fullstring', None, timeout=None, expected_status='any')

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.put_on_session')
    def test_put_with_cookies(self, put_on_session, create_session):
        library = APILibrary()
        library.call_put_request({"a": "Text"}, "Endpoint", "fullstring", None, "chocolate_chip")
        put_on_session.assert_called_with("putapi", "fullstring", None, timeout=None, expected_status='any')
        create_session.assert_called_with("putapi", "Endpoint", {"a": "Text"}, cookies="chocolate_chip", timeout=None)

    @patch('RequestsLibrary.SessionKeywords.SessionKeywords.create_session')
    @patch(f'{requestsSessionKeywords}.put_on_session')
    def test_put_with_kwarg(self, put_on_session, create_session):
        library = APILibrary()
        r = library.call_put_request({"a": "Text"}, "Endpoint", "fullstring", allow_redirects=False)
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text == "success"
        assert r.status_code == 200
        create_session.assert_called_with('putapi', 'Endpoint', {'a': 'Text'}, cookies=None, timeout=None)
        put_on_session.assert_called_with('putapi', 'fullstring', None, timeout=None, expected_status='any',
                                          allow_redirects=False)
