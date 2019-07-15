from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
from unittest.mock import Mock
import appium
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_open_application_register_sucessful(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = Mock()
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)
