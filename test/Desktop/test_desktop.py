from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import appium
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_open_application_successful(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)

    def test_maximize_window_successful(self):
        am = DesktopLibrary()
        am.maximize_window = MagicMock(return_value=True)
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)
        self.assertTrue(am.maximize_window())

    # @patch('DesktopLibrary.open_application')
    def test_open_application_splash_successful(self):
        am = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        am.open_application = MagicMock(side_effect=Exception)
        # am.open_application = MagicMock(side_effect=Exception())
        # am.open_application.side_effect = Exception()
        self.assertRaises(Exception, am.open_application)
        # with am.raises(Exception()) as e:
        #     self.assertEqual(Exception(), e)
        # self.assertEqual(am.open_application('remote_url', 'window_name=test'), 'WebDriverException')

        # self.assertTrue(am._cache.current)
