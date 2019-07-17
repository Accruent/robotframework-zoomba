from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
import appium
from unittest.mock import MagicMock
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_open_application_successful(self):
        dl = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)

    def test_open_application_splash_catch(self):
        dl = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url', window_ndle='test', app='testApp')
        self.assertTrue(dl._cache.current)

    def test_maximize_window_successful(self):
        dl = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)
        self.assertTrue(dl.maximize_window())

    def test_wait_for_and_input_text_simple(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_clear_text(mock_desk, "some_locator")
