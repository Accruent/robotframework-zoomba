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
        mock_desk.clear_text.assert_called_with("some_locator")

    def test_wait_for_and_click_element(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_element(mock_desk, "some_locator")
        mock_desk.click_element.assert_called_with("some_locator")

    def test_wait_for_and_click_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_text(mock_desk, "some_text")
        mock_desk.click_text.assert_called_with("some_text", False)

    def test_wait_for_and_click_text_exact(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_text(mock_desk, "some_text", True)
        mock_desk.click_text.assert_called_with("some_text", True)

    def test_wait_for_and_click_button(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_click_button(mock_desk, "some_button")
        mock_desk.click_button.assert_called_with("some_button")

    def test_wait_for_and_input_password(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_input_password(mock_desk, "some_locator", "some_text")
        mock_desk.input_password.assert_called_with("some_locator", "some_text")

    def test_wait_for_and_input_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_input_text(mock_desk, "some_locator", "some_text")
        mock_desk.input_text.assert_called_with("some_locator", "some_text")

    def test_wait_for_and_input_value(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_input_value(mock_desk, "some_locator", "some_value")
        mock_desk.input_value.assert_called_with("some_locator", "some_value")

    def test_wait_for_and_long_press(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_long_press(mock_desk, "some_locator", 1000)
        mock_desk.long_press.assert_called_with("some_locator", 1000)

    def test_wait_until_element_contains(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_contains(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_contain_text.assert_called_with("some_locator", 'test_text', None)

    def test_wait_until_element_does_not_contain(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_does_not_contain(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_not_contain_text.assert_called_with("some_locator", 'test_text', None)

    def test_wait_until_element_is_enabled(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_is_enabled(mock_desk, "some_locator")
        mock_desk.element_should_be_enabled.assert_called_with("some_locator")

    def test_wait_until_element_is_disabled(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_until_element_is_disabled(mock_desk, "some_locator")
        mock_desk.element_should_be_disabled.assert_called_with("some_locator")

    def test_drag_and_drop(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        ActionChains.drag_and_drop = MagicMock()
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.drag_and_drop(mock_desk, "some_locator", "some_other_locator")
        ActionChains.drag_and_drop.assert_called()

    def test_drag_and_drop_missing_source(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._element_find.side_effect = ValueError
        MobileLibrary.open_application(mock_desk, 'remote_url')
        self.assertRaises(ValueError, MobileLibrary.drag_and_drop, mock_desk, "some_locator", "some_other_locator")

    def test_drag_and_drop_missing_target(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._element_find.side_effect = [True, ValueError]
        MobileLibrary.open_application(mock_desk, 'remote_url')
        self.assertRaises(ValueError, MobileLibrary.drag_and_drop, mock_desk, "some_locator", "some_other_locator")

    def test_drag_and_drop_with_offset(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        ActionChains.drag_and_drop_by_offset = MagicMock()
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.drag_and_drop_by_offset(mock_desk, "some_locator", x_offset=100, y_offset=100)
        ActionChains.drag_and_drop_by_offset.assert_called()

    def test_drag_and_drop_with_offset_missing_locator(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._element_find.side_effect = ValueError
        MobileLibrary.open_application(mock_desk, 'remote_url')
        self.assertRaises(ValueError, MobileLibrary.drag_and_drop_by_offset, mock_desk, "some_locator",
                          x_offset=100, y_offset=100)

    def test_scroll_up_to_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._is_text_present.side_effect = [False, True]
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.scroll_up_to_text(mock_desk, "some_locator")
        mock_desk.swipe_by_percent.assert_called()

    def test_scroll_up_to_text_failure(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._is_text_present.side_effect = [False, False, False]
        MobileLibrary.open_application(mock_desk, 'remote_url')
        self.assertRaises(AssertionError, MobileLibrary.scroll_up_to_text, mock_desk, "some_locator", 2)

    def test_scroll_down_to_text(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._is_text_present.side_effect = [False, True]
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.scroll_down_to_text(mock_desk, "some_locator")
        mock_desk.swipe_by_percent.assert_called()

    def test_scroll_down_to_text_failure(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        mock_desk._is_text_present.side_effect = [False, False, False]
        MobileLibrary.open_application(mock_desk, 'remote_url')
        self.assertRaises(AssertionError, MobileLibrary.scroll_down_to_text, mock_desk, "some_locator", 2)

    def test_wait_for_and_tap(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_tap(mock_desk, "some_locator")
        mock_desk.tap.assert_called_with("some_locator", None, None, 1)

    def test_wait_for_and_tap_multiple(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_tap(mock_desk, "some_locator", count=4)
        mock_desk.tap.assert_called_with("some_locator", None, None, 4)

    def test_wait_for_and_tap_override_defaults(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.open_application(mock_desk, 'remote_url')
        MobileLibrary.wait_for_and_tap(mock_desk, "some_locator", x_offset=200, y_offset=100, count=4,
                                       error='some_error', timeout='10s')
        mock_desk.tap.assert_called_with("some_locator", 200, 100, 4)

    # def test_capture_page_screenshot(self):
    #     mock_desk = MagicMock()
    #     mock_desk._get_screenshot_paths = MagicMock()
    #     webdriver.Remote = WebdriverRemoteMock
    #     MobileLibrary.capture_page_screenshot(mock_desk)
        # mock_desk._get_screenshot_paths.assert_called()

    def test_save_appium_screenshot(self):
        mock_desk = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        MobileLibrary.save_appium_screenshot(mock_desk)
        mock_desk.capture_page_screenshot.assert_called()
