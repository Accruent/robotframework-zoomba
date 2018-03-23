import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.SOAPLibrary import SOAPLibrary
from Zoomba.SOAPLibrary import _ObjectNamespacePlugin
from Zoomba import *
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import PropertyMock

class TestObjectNamespace(unittest.TestCase):

    class Simple:
        pass

    def test_should_be_equal_simple(self):
        mock_plugin = Mock()
        item = self.Simple()
        item.document = b'<stuff xmlns:tns="string" targetNamespace="string" xmlns="other">'
        type(mock_plugin).defaultNamespace = PropertyMock(return_value=b"someNamespace")
        _ObjectNamespacePlugin.loaded(mock_plugin, item)

















