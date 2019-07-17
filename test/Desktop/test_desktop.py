from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
import appium
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_open_application_successful(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)

    def test_open_application_splash_catch(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url', window_name='test', app='testApp')
        self.assertTrue(am._cache.current)

    def test_maximize_window_successful(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)
        self.assertTrue(am.maximize_window())
