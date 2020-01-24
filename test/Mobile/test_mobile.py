from Zoomba.MobileLibrary import MobileLibrary
import unittest
from appium import webdriver
from unittest.mock import MagicMock
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'Helpers'))
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):

    def test_wait_for_and_input_text_simple(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_clear_text(mock_desk, "some_locator")

    def test_wait_for_and_click_element(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_element(mock_desk, "some_locator")

    def test_wait_for_and_click_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_text(mock_desk, "some_text")

    def test_wait_for_and_click_text_exact(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_text(mock_desk, "some_text", True)

    def test_wait_for_and_input_password(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_input_password(mock_desk, "some_locator", "some_text")

    def test_wait_for_and_input_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_input_text(mock_desk, "some_locator", "some_text")

    def test_wait_for_and_long_press(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_long_press(mock_desk, "some_locator", 1000)

    def test_wait_until_element_contains(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_contains(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_does_not_contain(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_does_not_contain(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_is_enabled(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_is_enabled(mock_desk, "some_locator", 'test_text')

    def test_wait_until_element_is_disabled(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_is_disabled(mock_desk, "some_locator", 'test_text')

    def test_element_find_by_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary._element_find_by_text(mock_desk, "some_text")

    def test_element_find_by_text_exact(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary._element_find_by_text(mock_desk, "some_text", True)

    def test_drag_and_drop(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        ActionChains.drag_and_drop = MagicMock()
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.drag_and_drop(mock_desk, "some_locator", "some_other_locator")

    def test_drag_and_drop_with_offset(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        ActionChains.drag_and_drop_by_offset = MagicMock()
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.drag_and_drop_by_offset(mock_desk, "some_locator", x_offset=100, y_offset=100)
