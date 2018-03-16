import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.APILibrary import APILibrary
import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestDates(unittest.TestCase):
    def test_date_string_comparator_simple(self):
        library = APILibrary()
        library.date_string_comparator("a", "a", None, None)

    def test_date_string_comparator_fail_all_formats(self):
        library = APILibrary()
        unmatched = []
        library.date_string_comparator("a", "b", "key", unmatched)
        assert unmatched == [('------------------\nKey: key', 'Expected Date Not Correct Format:',
                              'Expected Formats: %Y-%m-%dT%H:%M:%S', '                  %Y-%m-%dT%H:%M:%SZ',
                              '                  %Y-%m-%dT%H:%M:%S.%f', '                  %Y-%m-%dT%H:%M:%S.%fZ',
                              'Date: a'),
                             ('------------------\nKey: key', 'Actual Date Not Correct Format:',
                              'Expected Formats: %Y-%m-%dT%H:%M:%S', '                  %Y-%m-%dT%H:%M:%SZ',
                              '                  %Y-%m-%dT%H:%M:%S.%f', '                  %Y-%m-%dT%H:%M:%S.%fZ',
                              'Date: b')]

    def test_date_string_comparator_fail_outside_dates(self):
        library = APILibrary()
        unmatched = []
        library.date_string_comparator("2018-08-08T05:05:05", "2018-08-09T05:05:05", "key", unmatched)
        assert unmatched == [('------------------\nDates Not Close Enough\nKey: key',
                              'Expected: 2018-08-08 05:05:05', 'Actual: 2018-08-09 05:05:05')]
















