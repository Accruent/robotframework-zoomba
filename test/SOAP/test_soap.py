import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.SOAPLibrary import SOAPLibrary
from Zoomba.SOAPLibrary import _ObjectNamespacePlugin
from Zoomba.SOAPLibrary import *
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import PropertyMock

class TestObjectNamespace(unittest.TestCase):

    class Simple:
        pass

    def test_loaded_namespace_simple(self):
        mock_plugin = Mock()
        item = self.Simple()
        item.document = b'<stuff xmlns:tns="string" targetNamespace="string" xmlns="other">'
        type(mock_plugin).defaultNamespace = PropertyMock(return_value=b"someNamespace")
        _ObjectNamespacePlugin.loaded(mock_plugin, item)

    def test_no_default_namespace_simple(self):
        mock_plugin = Mock()
        item = self.Simple()
        item.document = b'<stuff xmlns:tns="string" targetNamespace="string" xmlns="other">'
        type(mock_plugin).defaultNamespace = None
        _ObjectNamespacePlugin.loaded(mock_plugin, item)
        assert mock_plugin.defaultNamespace == b'string'

    def test_no_tns_or_namespace_simple(self):
        mock_plugin = Mock()
        item = self.Simple()
        item.document = b'<stuff xmlns="other">'
        type(mock_plugin).defaultNamespace = b"string"
        _ObjectNamespacePlugin.loaded(mock_plugin, item)
        assert item.document == b'<stuff xmlns:tns="string" targetNamespace="string" xmlns="other">'

    def test_no_tns_or_namespace_replace_type_namespace_simple(self):
        mock_plugin = Mock()
        item = self.Simple()
        item.document = b'<stuff xmlns="other"><something type="one">'
        type(mock_plugin).defaultNamespace = b"string"
        _ObjectNamespacePlugin.loaded(mock_plugin, item)
        assert item.document == b'<stuff xmlns:tns="string" targetNamespace="string" ' \
                                b'xmlns="other"><something type="tns:one">'

class TestSoapLibrary(unittest.TestCase):

    @patch('Zoomba.SOAPLibrary._build_dict_from_response')
    def test_convert_soap(self, build_dict):
        build_dict.return_value = {"a":"1"}
        sl = SOAPLibrary()
        response = sl.convert_soap_response_to_json({"a":"1"})
        assert response == '{"a": "1"}'








