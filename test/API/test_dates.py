import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
import datetime
import unittest
import warnings
from Zoomba.APILibrary import APILibrary
from Zoomba.APILibrary import _date_format
from Zoomba import ZoombaError


class TestDates(unittest.TestCase):
    def test_date_string_comparator_simple(self):
        library = APILibrary()
        library.date_string_comparator("a", "a", None, None)

    def test_date_string_comparator_dates_close_enough(self):
        library = APILibrary()
        unmatched = []
        library.date_string_comparator("2018-08-08T05:05:05", "2018-08-08T05:06:05", "key", unmatched)
        assert unmatched == []

    def test_date_string_comparator_fail_all_formats(self):
        library = APILibrary()
        unmatched = []
        library.date_string_comparator("a", "b", "key", unmatched)
        unmatched_a = ZoombaError(
                key="key",
                note="Expected Date Not Correct Format",
                expected_formats="%Y-%m-%dT%H:%M:%S\n" +
                                 "                  %Y-%m-%dT%H:%M:%SZ\n" +
                                 "                  %Y-%m-%dT%H:%M:%S.%f\n" +
                                 "                  %Y-%m-%dT%H:%M:%S.%fZ",
                date='a')
        unmatched_b = ZoombaError(
                key="key",
                note="Actual Date Not Correct Format",
                expected_formats="%Y-%m-%dT%H:%M:%S\n" +
                                 "                  %Y-%m-%dT%H:%M:%SZ\n" +
                                 "                  %Y-%m-%dT%H:%M:%S.%f\n" +
                                 "                  %Y-%m-%dT%H:%M:%S.%fZ",
                date='b')
        assert unmatched == [unmatched_a,unmatched_b]

    def test_date_string_comparator_fail_outside_dates(self):
        library = APILibrary()
        unmatched = []
        library.date_string_comparator("2018-08-08T05:05:05", "2018-08-09T05:05:05", "key", unmatched)
        assert unmatched == [('------------------\nDates Not Close Enough\nKey: key',
                              'Expected: 2018-08-08 05:05:05', 'Actual: 2018-08-09 05:05:05')]

    def test_date_comparator_dates_close_enough_with_custom_margin(self):
        library = APILibrary()
        date_one = datetime.datetime.strptime("2018-05-05T05:05:05", '%Y-%m-%dT%H:%M:%S')
        date_two = datetime.datetime.strptime("2018-05-05T03:05:05", '%Y-%m-%dT%H:%M:%S')
        unmatched = []
        library.date_comparator(date_one, date_two, "key", unmatched, "hours", 10)
        assert unmatched == []

    def test_date_comparator_dates_close_enough_with_custom_margin_fail(self):
        library = APILibrary()
        date_one = datetime.datetime(2018, 5, 6, 5, 5, 5)
        date_two = datetime.datetime(2018, 5, 5, 3, 5, 5)
        unmatched = []
        library.date_comparator(date_one, date_two, "key", unmatched, "hours", 10)
        assert unmatched == [('------------------\nDates Not Close Enough\nKey: key',
                              'Expected: 2018-05-06 05:05:05', 'Actual: 2018-05-05 03:05:05')]

    def test__date_format_standard_date_formats(self):
        date = datetime.datetime(2018, 5, 5, 5, 5, 5)
        date_with_ms = datetime.datetime(2018, 5, 5, 5, 5, 5, 50000)
        assert date == _date_format("2018-05-05T05:05:05", "key", [], "string")
        assert date == _date_format("2018-05-05T05:05:05Z", "key", [], "string")
        assert date == _date_format("2018-05-05T05:05:05-08:00", "key", [], "string")
        assert date == _date_format("2018-05-05T05:05:05Z-08:00", "key", [], "string")
        assert date_with_ms == _date_format("2018-05-05T05:05:05.05", "key", [], "string")
        assert date_with_ms == _date_format("2018-05-05T05:05:05.05Z", "key", [], "string")
        assert date_with_ms == _date_format("2018-05-05T05:05:05.05-08:00", "key", [], "string")
        assert date_with_ms == _date_format("2018-05-05T05:05:05.05Z-08:00", "key", [], "string")

    def test__date_format_unique_date_formats(self):
        date = datetime.datetime(2018, 5, 5, 5, 5, 5)
        date_with_extra_ms = datetime.datetime(2019, 9, 20, 17, 35, 0, 894400)
        assert date == _date_format("2018/05/05 05:05:05", "key", [], "string", "%Y/%m/%d %H:%M:%S")
        assert date_with_extra_ms == _date_format("2019-09-20T17:35:00.8944008Z", "key", [], "string")

    def test__date_format_unique_date_formats_fail(self):
        unmatched = []
        _date_format("210568/05/05 05:05:05", "key", unmatched, "string", "%Y/%m/%d %H:%M:%S")

        assert unmatched == [ZoombaError(
            key="key",
            note="string Date Not Correct Format",
            expected_format="%Y/%m/%d %H:%M:%S",
            date='210568/05/05 05:05:05')]

    def test_nonzero_nanoseconds_cutoff_no_warning(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            date = datetime.datetime(2018, 5, 5, 5, 5, 5, 123456)
            assert date == _date_format("2018-05-05T05:05:05.123456789", "key", [], "string")
