import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.APILibrary import APILibrary
import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestInternal(unittest.TestCase):
    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_generate_unmatched_keys_error_message_simple(self, fail):
        library = APILibrary()
        library.generate_unmatched_keys_error_message('a')
        assert fail.called_with("""Key(s) Did Not Match: a Please see differing value(s)""")
