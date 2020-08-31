from selenium.common.exceptions import WebDriverException, NoSuchElementException
from Zoomba.DesktopLibrary import DesktopLibrary
import unittest
from appium import webdriver
import subprocess
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'Helpers'))
from webdriverremotemock import WebdriverRemoteMock


class TestInternal(unittest.TestCase):
    def test_get_keyword_names_successful(self):
        DesktopLibrary().get_keyword_names()

    def test_open_application_successful(self):
        dl = DesktopLibrary()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)

    def test_open_application_successful_double(self):
        dl = DesktopLibrary()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)

    def test_open_application_splash_catch(self):
        dl = DesktopLibrary()
        subprocess.Popen = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url', window_name='test', app='testApp', splash_delay=1)
        self.assertTrue(dl._cache.current)

    def test_open_application_splash_catch_double(self):
        dl = DesktopLibrary()
        subprocess.Popen = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url', window_name='test', app='testApp', splash_delay=1)
        self.assertTrue(dl._cache.current)
        dl.open_application('remote_url', window_name='test2', app='testApp', splash_delay=1)
        self.assertTrue(dl._cache.current)

    def test_switch_application_failure(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_name = MagicMock(side_effect=[WebDriverException, WebDriverException])
        self.assertRaisesRegex(AssertionError, 'Error finding window "test" in the desktop session. Is it a top level '
                                               'window handle?.', dl.switch_application_by_name,
                                               'remote_url', window_name='test')

    def test_switch_application_failure_2(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        dl._wait_until_page_contains_element = MagicMock()
        webdriver.Remote.find_element_by_name = MagicMock()
        webdriver.Remote.find_element_by_name.side_effect = [WebDriverException, "Window"]
        self.assertRaisesRegex(AssertionError, 'Error finding window "test" in the desktop session. Is it a top level '
                                               'window handle?.', dl.switch_application_by_name,
                                               'remote_url', window_name='test')

    def test_switch_application_failure_3(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        web_driver_mock = WebdriverRemoteMock
        webdriver.Remote = MagicMock(side_effect=[web_driver_mock, Exception])
        web_driver_mock.find_element_by_name = MagicMock()
        web_driver_mock.quit = MagicMock(return_value=True)
        self.assertRaisesRegex(AssertionError, 'Error connecting webdriver to window "test".',
                               dl.switch_application_by_name, 'remote_url', window_name='test')

    def test_launch_application_successful(self):
        dl = DesktopLibrary()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        dl.quit_application()
        dl.launch_application()
        self.assertTrue(dl._cache.current)

    def test_maximize_window_successful(self):
        mock_desk = MagicMock()
        self.assertTrue(DesktopLibrary.maximize_window(mock_desk))

    def test_wait_for_and_clear_text_simple(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_clear_text(mock_desk, "some_locator")
        mock_desk.clear_text.assert_called_with("some_locator")

    def test_wait_for_and_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_click_element(mock_desk, "some_locator")
        mock_desk.click_element.assert_called_with("some_locator")

    def test_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.click_element(mock_desk, "some_locator")
        mock_desk._element_find.assert_called_with("some_locator", True, True)

    def test_click_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.click_text(mock_desk, "some_text")
        mock_desk._element_find_by_text.assert_called_with("some_text", False)

    def test_click_text_exact(self):
        mock_desk = MagicMock()
        DesktopLibrary.click_text(mock_desk, "some_text", True)
        mock_desk._element_find_by_text.assert_called_with("some_text", True)

    def test_wait_for_and_click_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_click_text(mock_desk, "some_text")
        mock_desk.click_text.assert_called_with("some_text", False)

    def test_wait_for_and_click_text_exact(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_click_text(mock_desk, "some_text", True)
        mock_desk.click_text.assert_called_with("some_text", True)

    def test_wait_for_and_input_password(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_input_password(mock_desk, "some_locator", "some_text")
        mock_desk.input_password.assert_called_with("some_locator", "some_text")

    def test_wait_for_and_input_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_input_text(mock_desk, "some_locator", "some_text")
        mock_desk.input_text.assert_called_with("some_locator", "some_text")

    def test_wait_for_and_long_press(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_long_press(mock_desk, "some_locator", 1000)
        mock_desk.long_press.assert_called_with("some_locator", 1000)

    def test_wait_until_element_contains(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_contains(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_contain_text.assert_called_with("some_locator", "test_text", None)

    def test_wait_until_element_does_not_contain(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_does_not_contain(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_not_contain_text.assert_called_with("some_locator", "test_text", None)

    def test_wait_until_element_is_enabled(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_is_enabled(mock_desk, "some_locator")
        mock_desk.element_should_be_enabled.assert_called_with("some_locator")

    def test_wait_until_element_is_disabled(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_is_disabled(mock_desk, "some_locator")
        mock_desk.element_should_be_disabled.assert_called_with("some_locator")

    def test_mouse_over_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_element(mock_desk, "some_locator")
        mock_desk._move_to_element.assert_called_with(unittest.mock.ANY, unittest.mock.ANY, 0, 0)

    def test_mouse_over_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk._move_to_element.assert_called_with(unittest.mock.ANY, unittest.mock.ANY, 100, 100)

    def test_mouse_over_and_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_element(mock_desk, "some_locator")
        mock_desk.mouse_over_element.assert_called_with("some_locator", x_offset=0, y_offset=0)
        mock_desk.click_a_point.assert_called_with(double_click=False)

    def test_mouse_over_and_click_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_element.assert_called_with("some_locator", x_offset=100, y_offset=100)
        mock_desk.click_a_point.assert_called_with(double_click=False)

    def test_mouse_over_and_context_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_context_click_element(mock_desk, "some_locator")
        mock_desk.mouse_over_element.assert_called_with("some_locator", x_offset=0, y_offset=0)
        mock_desk.context_click_a_point.assert_called_with()

    def test_mouse_over_and_context_click_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_context_click_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_element.assert_called_with("some_locator", x_offset=100, y_offset=100)
        mock_desk.context_click_a_point.assert_called_with()

    def test_mouse_over_and_click_element_with_double_click(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_element(mock_desk, "some_locator", True)
        mock_desk.mouse_over_element.assert_called_with("some_locator", x_offset=0, y_offset=0)
        mock_desk.click_a_point.assert_called_with(double_click=True)

    def test_wait_for_and_mouse_over_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_element(mock_desk, "some_locator")
        mock_desk.mouse_over_element.assert_called_with("some_locator", 0, 0)

    def test_wait_for_and_mouse_over_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_element.assert_called_with("some_locator", 100, 100)

    def test_wait_for_and_mouse_over_and_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator")
        mock_desk.mouse_over_and_click_element.assert_called_with("some_locator", False, 0, 0)

    def test_wait_for_and_mouse_over_and_click_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_and_click_element.assert_called_with("some_locator", False, 100, 100)

    def test_wait_for_and_mouse_over_and_click_element_with_double_click(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator", double_click=True)
        mock_desk.mouse_over_and_click_element.assert_called_with("some_locator", True, 0, 0)

    def test_mouse_over_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_text(mock_desk, "some_text")
        mock_desk._move_to_element.assert_called_with(unittest.mock.ANY, unittest.mock.ANY, 0, 0)

    def test_mouse_over_text_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_text(mock_desk, "some_text", True, x_offset=100, y_offset=100)
        mock_desk._move_to_element.assert_called_with(unittest.mock.ANY, unittest.mock.ANY, 100, 100)

    def test_mouse_over_and_click_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_text(mock_desk, "some_text")
        mock_desk.mouse_over_text.assert_called_with("some_text", exact_match=False, x_offset=0, y_offset=0)
        mock_desk.click_a_point.assert_called_with(double_click=False)

    def test_mouse_over_and_click_text_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_text(mock_desk, "some_text", x_offset=100, y_offset=100)
        mock_desk.mouse_over_text.assert_called_with("some_text", exact_match=False, x_offset=100, y_offset=100)
        mock_desk.click_a_point.assert_called_with(double_click=False)

    def test_mouse_over_and_context_click_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_context_click_text(mock_desk, "some_text")
        mock_desk.mouse_over_text.assert_called_with("some_text", exact_match=False, x_offset=0, y_offset=0)
        mock_desk.context_click_a_point.assert_called_with()

    def test_mouse_over_and_context_click_text_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_context_click_text(mock_desk, "some_text", x_offset=100, y_offset=100)
        mock_desk.mouse_over_text.assert_called_with("some_text", exact_match=False, x_offset=100, y_offset=100)
        mock_desk.context_click_a_point.assert_called_with()

    def test_mouse_over_and_click_text_with_double_click(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_and_click_text(mock_desk, "some_text", True, double_click=True)
        mock_desk.mouse_over_text.assert_called_with("some_text", exact_match=True, x_offset=0, y_offset=0)
        mock_desk.click_a_point.assert_called_with(double_click=True)

    def test_wait_for_and_mouse_over_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_text(mock_desk, "some_text")
        mock_desk.mouse_over_text.assert_called_with("some_text", False, 0, 0)

    def test_wait_for_and_mouse_over_text_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_text(mock_desk, "some_text", x_offset=100, y_offset=100)
        mock_desk.mouse_over_text.assert_called_with("some_text", False, 100, 100)

    def test_wait_for_and_mouse_over_and_click_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_text(mock_desk, "some_text")
        mock_desk.mouse_over_and_click_text.assert_called_with("some_text", False, False, 0, 0)

    def test_wait_for_and_mouse_over_and_click_text_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_text(mock_desk, "some_text", x_offset=100, y_offset=100)
        mock_desk.mouse_over_and_click_text.assert_called_with("some_text", False, False, 100, 100)

    def test_wait_for_and_mouse_over_and_click_text_with_double_click(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_text(mock_desk, "some_text", True, double_click=True)
        mock_desk.mouse_over_and_click_text.assert_called_with("some_text", True, True, 0, 0)

    def test_element_find_by_text(self):
        mock_desk = MagicMock()
        DesktopLibrary._element_find_by_text(mock_desk, "some_text")
        mock_desk._element_find.assert_called_with(unittest.mock.ANY, True, True)

    def test_element_find_by_text_exact(self):
        mock_desk = MagicMock()
        DesktopLibrary._element_find_by_text(mock_desk, "some_text", True)
        mock_desk._element_find.assert_called_with(unittest.mock.ANY, True, True)

    def test_element_find_by_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['name', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "Name='Capture'", True, True)
        mock_desk._current_application().find_element_by_name.assert_called_with('Capture')

    def test_elements_find_by_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['name', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "Name='Capture'", False, True)
        mock_desk._current_application().find_elements_by_name.assert_called_with('Capture')

    def test_element_find_by_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['accessibility_id', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "accessibility_id='Capture'", True, True)
        mock_desk._current_application().find_element_by_accessibility_id.assert_called_with('Capture')

    def test_elements_find_by_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['accessibility_id', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "accessibility_id='Capture'", False, True)
        mock_desk._current_application().find_elements_by_accessibility_id.assert_called_with('Capture')

    def test_element_find_by_class_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['class', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "class='Capture'", True, True)
        mock_desk._current_application().find_element_by_class_name.assert_called_with('Capture')

    def test_elements_find_by_class_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['class', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "class='Capture'", False, True)
        mock_desk._current_application().find_elements_by_class_name.assert_called_with('Capture')

    def test_element_find_by_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['xpath', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "xpath=//TreeItem[@Name='Capture']", True, True)
        mock_desk._current_application().find_element_by_xpath.assert_called_with('Capture')

    def test_elements_find_by_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['xpath', 'Capture'])
        DesktopLibrary._element_find(mock_desk, "xpath=//TreeItem[@Name='Capture']", False, True)
        mock_desk._current_application().find_elements_by_xpath.assert_called_with('Capture')

    def test_element_find_by_default_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "//TreeItem[@Name='Capture']"])
        DesktopLibrary._element_find(mock_desk, "//TreeItem[@Name='Capture']", True, True)
        mock_desk._current_application().find_element_by_xpath.assert_called_with("//TreeItem[@Name='Capture']")

    def test_elements_find_by_default_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "//TreeItem[@Name='Capture']"])
        DesktopLibrary._element_find(mock_desk, "//TreeItem[@Name='Capture']", False, True)
        mock_desk._current_application().find_elements_by_xpath.assert_called_with("//TreeItem[@Name='Capture']")

    def test_element_find_by_default_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "Capture"])
        DesktopLibrary._element_find(mock_desk, "Capture", True, True)
        mock_desk._current_application().find_element_by_accessibility_id.assert_called_with('Capture')

    def test_elements_find_by_default_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "Capture"])
        DesktopLibrary._element_find(mock_desk, "Capture", False, True)
        mock_desk._current_application().find_elements_by_accessibility_id.assert_called_with('Capture')

    def test_element_find_fail(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['blockbuster_id', '123456789'])
        self.assertRaisesRegex(AssertionError, "Element locator with prefix 'blockbuster_id' is not supported",
                               DesktopLibrary._element_find, mock_desk, "blockbuster_id=123456789", True, True)

    def test_parse_locator_xpath(self):
        mock_desk = MagicMock()
        parse = DesktopLibrary._parse_locator(mock_desk, '//test')
        self.assertEqual(parse, (None, '//test'))

    def test_parse_locator(self):
        mock_desk = MagicMock()
        parse = DesktopLibrary._parse_locator(mock_desk, 'name=test')
        self.assertEqual(parse, ('name', 'test'))

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_by_offset")
    def test_mouse_over_by_offset(self, action):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_by_offset(mock_desk, 100, 100)
        action.assert_called_with(100, 100)

    @patch("selenium.webdriver.common.action_chains.ActionChains.click")
    def test_click_a_point(self, action):
        mock_desk = MagicMock()
        DesktopLibrary.click_a_point(mock_desk)
        action.assert_called_with()

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_by_offset")
    @patch("selenium.webdriver.common.action_chains.ActionChains.click")
    def test_click_a_point_with_offset(self, click, move):
        mock_desk = MagicMock()
        DesktopLibrary.click_a_point(mock_desk, x_offset=100, y_offset=100)
        move.assert_called_with(100, 100)
        click.assert_called_with()

    @patch("selenium.webdriver.common.action_chains.ActionChains.double_click")
    def test_click_a_point_with_double_click(self, click):
        mock_desk = MagicMock()
        DesktopLibrary.click_a_point(mock_desk, double_click=True)
        click.assert_called_with()

    @patch("selenium.webdriver.common.action_chains.ActionChains.context_click")
    def test_context_click_a_point(self, click):
        mock_desk = MagicMock()
        DesktopLibrary.context_click_a_point(mock_desk)
        click.assert_called_with()

    @patch("selenium.webdriver.common.action_chains.ActionChains.move_by_offset")
    @patch("selenium.webdriver.common.action_chains.ActionChains.context_click")
    def test_context_click_a_point_with_offset(self, click, move):
        mock_desk = MagicMock()
        DesktopLibrary.context_click_a_point(mock_desk, x_offset=-400, y_offset=-400)
        move.assert_called_with(-400, -400)
        click.assert_called_with()

    @patch("selenium.webdriver.common.action_chains.ActionChains.drag_and_drop")
    def test_drag_and_drop(self, drag):
        mock_desk = MagicMock()
        DesktopLibrary.drag_and_drop(mock_desk, "some_locator", "some_other_locator")
        drag.assert_called_with(unittest.mock.ANY, unittest.mock.ANY)

    @patch("selenium.webdriver.common.action_chains.ActionChains.drag_and_drop_by_offset")
    def test_drag_and_drop_with_offset(self, drag):
        mock_desk = MagicMock()
        DesktopLibrary.drag_and_drop_by_offset(mock_desk, "some_locator", x_offset=100, y_offset=100)
        drag.assert_called_with(unittest.mock.ANY, 100, 100)

    @patch("selenium.webdriver.common.action_chains.ActionChains")
    def test_move_to_element(self, move):
        mock_desk = MagicMock()
        DesktopLibrary._move_to_element(mock_desk, move, "some_locator", 0, 0)
        move.move_to_element.assert_called_with("some_locator")

    @patch("selenium.webdriver.common.action_chains.ActionChains")
    def test_move_to_element_with_offset(self, move):
        mock_desk = MagicMock()
        DesktopLibrary._move_to_element(mock_desk, move, "some_locator", 100, 100)
        move.move_to_element_with_offset.assert_called_with("some_locator", 100, 100)

    @patch("selenium.webdriver.common.action_chains.ActionChains.send_keys")
    def test_send_keys(self, send_keys):
        mock_desk = MagicMock()
        DesktopLibrary.send_keys(mock_desk, 'test', '\ue007')
        send_keys.assert_called_with('\ue007')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_send_keys_without_args(self, fail):
        mock_desk = MagicMock()
        DesktopLibrary.send_keys(mock_desk)
        fail.assert_called_with('No key arguments specified.')

    @patch("selenium.webdriver.common.action_chains.ActionChains.send_keys_to_element")
    def test_send_keys_to_element(self, send_keys):
        mock_desk = MagicMock()
        DesktopLibrary.send_keys_to_element(mock_desk, 'some_element', 'test', '\ue007')
        send_keys.assert_called_with(unittest.mock.ANY, '\ue007')

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_send_keys_to_element_without_args(self, fail):
        mock_desk = MagicMock()
        DesktopLibrary.send_keys_to_element(mock_desk, 'some_locator')
        fail.assert_called_with('No key arguments specified.')

    def test_capture_page_screenshot(self):
        mock_desk = MagicMock()
        mock_desk._get_screenshot_paths = MagicMock(return_value=['path', 'link'])
        DesktopLibrary.capture_page_screenshot(mock_desk)
        mock_desk._get_screenshot_paths.assert_called_with(None)

    def test_capture_page_screenshot_else_case(self):
        mock_desk = MagicMock()
        mock_desk._get_screenshot_paths = MagicMock(return_value=['path', 'link'])
        del mock_desk._current_application().get_screenshot_as_file
        DesktopLibrary.capture_page_screenshot(mock_desk, 'filename')
        mock_desk._get_screenshot_paths.assert_called_with('filename')

    def test_save_appium_screenshot(self):
        mock_desk = MagicMock()
        DesktopLibrary.save_appium_screenshot(mock_desk)
        mock_desk.capture_page_screenshot.assert_called_with(unittest.mock.ANY)

    def test_select_from_combobox_no_desktop(self):
        mock_desk = MagicMock()
        DesktopLibrary.select_element_from_combobox(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_from_combobox_with_desktop(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[True, ValueError, True])
        DesktopLibrary.select_element_from_combobox(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_from_combobox_skip_to_desktop(self):
        mock_desk = MagicMock()
        DesktopLibrary.select_element_from_combobox(mock_desk, 'some_locator', 'another_locator', True)
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_from_combobox_retry(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[True, NoSuchElementException, True])
        DesktopLibrary.select_element_from_combobox(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_from_combobox_retry_desktop(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[True, NoSuchElementException, True])
        DesktopLibrary.select_element_from_combobox(mock_desk, 'some_locator', 'another_locator', True)
        mock_desk.click_element.assert_called_with('another_locator')

    def test_wait_until_page_contains_private(self):
        mock_desk = MagicMock()
        DesktopLibrary._wait_until_page_contains(mock_desk, 'some_text', 5)
        mock_desk._wait_until.asser_called_with('some_text', 5)

    def test_wait_until_page_contains_element_private(self):
        mock_desk = MagicMock()
        DesktopLibrary._wait_until_page_contains_element(mock_desk, 'some_element', 5)
        mock_desk._wait_until.asser_called_with('some_element', 5)
