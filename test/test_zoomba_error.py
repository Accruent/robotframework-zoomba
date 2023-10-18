# """Unit tests for GUILibrary keywords"""
import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from Zoomba import ZoombaError


class TestInternal(unittest.TestCase):
    def test_create_zoomba_error(self):
        err = ZoombaError("description", "key", "expected", "actual")
        assert f"{err}" == "Error: description\n------------------\nKey: key\nExpected: expected\nActual: actual"

    def test_create_zoomba_error_by_keyword(self):
        err = ZoombaError(expected="expected", actual="actual", error="description", key="key")
        assert f"{err}" == "Error: description\n------------------\nKey: key\nExpected: expected\nActual: actual"

    def test_create_zoomba_error_with_kwargs(self):
        err = ZoombaError("description", "key", "expected", "actual", test="test")
        assert f"{err}" == "Error: description\n------------------\nKey: key\n" \
                           "Expected: expected\nActual: actual\nTest: test"

    def test_compare_zoomba_error_with_string(self):
        err = ZoombaError("string")
        assert err == "Error: string"

