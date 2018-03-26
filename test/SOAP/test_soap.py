import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.SOAPLibrary import SOAPLibrary
from Zoomba.SOAPLibrary import _ObjectNamespacePlugin
from Zoomba.SOAPLibrary import _wsdl_sub_builder, _build_dict_from_response, _build_wsdl_objects
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import PropertyMock
from suds import WebFault

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

    @patch('Zoomba.SOAPLibrary.Client')
    @patch('Zoomba.SOAPLibrary.BuiltIn')
    @patch('Zoomba.SOAPLibrary._ObjectNamespacePlugin')
    def test_create_soap_session_and_fix_wsdl_simple(self, obj_nsp, builtIn, client):
        mock_soap = Mock()
        obj_nsp.return_value = "string"
        client.return_value = "accepted"
        SOAPLibrary.create_soap_session_and_fix_wsdl(mock_soap, "host", "endpoint", "alias")
        client.assert_called_with('hostendpoint?WSDL', plugins=['string'])
        builtIn.return_value.get_library_instance.return_value._add_client.assert_called_with("accepted", "alias")

    @patch('Zoomba.SOAPLibrary.Client')
    @patch('Zoomba.SOAPLibrary.BuiltIn')
    @patch('Zoomba.SOAPLibrary._ObjectNamespacePlugin')
    def test_create_soap_session_and_fix_wsdl_and_set_location(self, obj_nsp, builtIn, client):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session_and_fix_wsdl(mock_soap, "host", "endpoint", "alias", set_location="place")
        builtIn.return_value.get_library_instance.return_value.set_location.assert_called_with("place")

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_create_soap_session_simple(self, built):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session(mock_soap, "host", "endpoint")
        built.return_value.get_library_instance.return_value.create_soap_client.assert_called_with("hostendpoint?WSDL")

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_create_soap_session_simple(self, built):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session(mock_soap, "host", "endpoint")
        built.return_value.get_library_instance.return_value.create_soap_client.assert_called_with("hostendpoint?WSDL")

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_create_soap_session_alias(self, built):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session(mock_soap, "host", "endpoint", "alias")
        built.return_value.get_library_instance.return_value.create_soap_client.assert_called_with("hostendpoint?WSDL",
                                                                                                   "alias")

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_create_soap_session_function_and_set_location(self, built):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session(mock_soap, "host", "endpoint", set_location="here")
        built.return_value.get_library_instance.return_value.create_soap_client.assert_called_with("hostendpoint?WSDL")
        built.return_value.get_library_instance.return_value.set_location.assert_called_with("here")

    def test_create_soap_session_and_set_location_simple(self):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session_and_set_location(mock_soap, "host", "endpoint")
        mock_soap.create_soap_session.assert_called_with("host", "endpoint", None, set_location="hostendpoint")

    def test_create_soap_session_and_set_location_fix(self):
        mock_soap = Mock()
        SOAPLibrary.create_soap_session_and_set_location(mock_soap, "host", "endpoint", fix=True)
        mock_soap.create_soap_session_and_fix_wsdl.assert_called_with("host", "endpoint", None,
                                                                      set_location="hostendpoint")

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_call_soap_method_with_list_object_simple(self, built):
        mock_soap = Mock()
        SOAPLibrary.call_soap_method_with_list_object(mock_soap, "action", [1, 2])
        built.return_value.get_library_instance.return_value.call_soap_method.assert_called_with('action', 1, 2)

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    def test_call_soap_method_with_object_simple(self, built):
        mock_soap = Mock()
        err = WebFault(Mock(response=Mock(fault=None, document=None)), None)
        type(err).fault = PropertyMock(return_value="fault")
        built.return_value.get_library_instance.return_value._client.return_value.service.action = Mock(side_effect=err)
        assert SOAPLibrary.call_soap_method_with_object(mock_soap, "action", item=2) == "fault"

    @patch('Zoomba.SOAPLibrary.BuiltIn')
    @patch('Zoomba.SOAPLibrary._build_wsdl_objects')
    def test_create_wsdl_objects_simple(self, wsdl, built):
        mock_soap = Mock()
        client = built.return_value.get_library_instance.return_value._client.return_value
        client.factory.create.return_value = "create"
        SOAPLibrary.create_wsdl_objects(mock_soap, "type", {1: 2})
        client.factory.create.assert_called_with("type")
        wsdl.assert_called_with(client, "create", {1: 2})


class TestSoapPrivateMethods(unittest.TestCase):

    class Simple(object):
        pass

    class sudsobject(object):
        pass

    @patch('Zoomba.SOAPLibrary._build_wsdl_objects')
    def test__wsdl_sub_builder_simple(self, wsdl):
        mock_client = Mock()
        mock_client.factory.create.return_value = "create"
        _wsdl_sub_builder(mock_client, {'wsdl_object_type': 1, 'other': 2})
        mock_client.factory.create.assert_called_with(1)
        wsdl.assert_called_with(mock_client, "create", {'other': 2})

    def test__build_wsdl_objects_simple(self):
        simple = self.Simple()
        _build_wsdl_objects(None, simple, {"test": 2})
        assert simple.test == 2

    def test__build_wsdl_objects_list(self):
        simple = self.Simple()
        _build_wsdl_objects(None, simple, {"test": [1,2]})
        assert simple.test == [1, 2]

    @patch('Zoomba.SOAPLibrary._wsdl_sub_builder')
    def test__build_wsdl_objects_dict(self, wsdl):
        simple = self.Simple()
        wsdl.return_value = {"two": 2}
        _build_wsdl_objects(None, simple, {"test": {"two": 2}})
        assert simple.test == {"two": 2}

    @patch('Zoomba.SOAPLibrary._wsdl_sub_builder')
    def test__build_wsdl_objects_list_dict(self, wsdl):
        simple = self.Simple()
        wsdl.return_value = {"two": 2}
        _build_wsdl_objects(None, simple, {"test": [{"two": 2}]})
        assert simple.test == [{"two": 2}]

    @patch('robot.libraries.BuiltIn.BuiltIn.log')
    def test__build_wsdl_objects_dict_fail(self, log):
        simple = self.Simple()
        _build_wsdl_objects(None, simple, {"test": {"two": 2}})
        log.assert_called_with('Failed to define wsdl_object_type for child object. [test]', level='ERROR')

    def test__build_dict_from_response_simple(self):
        assert _build_dict_from_response({1: 2}) == {1: '2'}

    @patch('robot.libraries.BuiltIn.BuiltIn.log')
    def test__build_dict_from_response_not_iterable(self, log):
        _build_dict_from_response(10)
        log.assert_called_with(level='INFO', message='Argument Passed Was Not Iterable')

    def test__build_dict_from_response_list(self):
        assert _build_dict_from_response({1: [2, 3]}) == {1: ['2', '3']}

    def test__build_dict_from_response_instance(self):
        suds = self.sudsobject()
        assert _build_dict_from_response({1: suds}) == {1: suds}

    def test__build_dict_from_response_instance_list(self):
        suds = self.sudsobject()
        assert _build_dict_from_response({1: [suds]}) == {1: [suds]}
