from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
import appium
import os
from unittest.mock import MagicMock, patch
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_get_keyword_names_successful(self):
        DesktopLibrary().get_keyword_names()

    def test_open_application_successful(self):
        dl = DesktopLibrary()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)

    @patch('os.startfile')
    def test_open_application_splash_catch(self, os_call):
        dl = DesktopLibrary()
        os_call.startfile = MagicMock(return_value=True)
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url', window_name='test', app='testApp')
        self.assertTrue(dl._cache.current)
        self.assertTrue(os_call)

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

    def test_wait_for_and_click_element(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_click_element(mock_desk, "some_locator")

    def test_wait_for_and_click_text(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_click_text(mock_desk, "some_text")

    def test_wait_for_and_click_text_exact(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_click_text(mock_desk, "some_text", True)

    def test_wait_for_and_input_password(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_input_password(mock_desk, "some_locator", "some_text")

    def test_wait_for_and_input_text(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_input_text(mock_desk, "some_locator", "some_text")

    def test_wait_for_and_long_press(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_for_and_long_press(mock_desk, "some_locator", 1000)

    def test_wait_until_element_contains(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_until_element_contains(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_does_not_contain(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_until_element_does_not_contain(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_is_enabled(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_until_element_is_enabled(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_is_disabled(self):
        mock_desk = MagicMock()
        appium.webdriver.Remote = WebdriverRemoteMock
        DesktopLibrary.open_application(mock_desk, 'remote_url')
        DesktopLibrary.wait_until_element_is_disabled(mock_desk, "some_locator", 'test_text')
