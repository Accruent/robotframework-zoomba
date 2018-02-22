from src.Zoomba.APILibrary import *
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
        assert r.text
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.get_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_get_insecure_request(self, create_session, get_request, disable_warnings):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        library.call_get_request({"a": "Text"}, "Endpoint", "fullstring")
        assert disable_warnings.called

    def test_post_default(self):
        library = APILibrary()
        self.assertRaises(TypeError, library.call_post_request)

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    def test_basic_post(self, create_session, get_request):
        library = APILibrary()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        type(r).text = PropertyMock(return_value="success")
        type(r).status_code = PropertyMock(return_value=200)
        assert r.text
        assert r.status_code == 200

    @patch('RequestsLibrary.RequestsKeywords.create_session')
    @patch('RequestsLibrary.RequestsKeywords.post_request')
    @patch('requests.packages.urllib3.disable_warnings')
    def test_post_insecure_request(self, create_session, post_request, disable_warnings):
        library = APILibrary()
        library.suppress_insecure_request_warnings()
        r = library.call_post_request({"a": "Text"}, "Endpoint", "fullstring")
        assert disable_warnings.called
