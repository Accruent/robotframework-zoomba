import sys
import os
import psutil
import unittest
import subprocess
from selenium.common.exceptions import WebDriverException, NoSuchElementException, \
    InvalidSelectorException
from Zoomba.DesktopLibrary import DesktopLibrary
from appium import webdriver
from unittest.mock import MagicMock, patch
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'Helpers'))
from webdriverremotemock import WebdriverRemoteMock


def _long_running_function():
    while True:
        return 'Error'


class TestInternal(unittest.TestCase):
    def test_get_keyword_names_successful(self):
        DesktopLibrary().get_keyword_names()

    @patch('subprocess.call')
    @patch('subprocess.Popen')
    def test_driver_setup_and_teardown(self, Popen, call):
        Popen.return_value = 1
        dl = DesktopLibrary()
        dl.driver_setup()
        self.assertTrue(dl.winappdriver.process)
        dl.driver_teardown()
        self.assertFalse(dl.winappdriver.process)

    @patch('subprocess.Popen')
    def test_driver_setup_failure(self, Popen):
        Popen.side_effect = Exception
        dl = DesktopLibrary()
        dl.driver_setup()
        self.assertFalse(dl.winappdriver.process)

    @patch('subprocess.call')
    def test_teardown_without_setup(self, call):
        dl = DesktopLibrary()
        dl.driver_teardown()
        self.assertFalse(dl.winappdriver.process)

    def test_driver_child_process_teardown(self):
        mock_child = MagicMock()
        dl = DesktopLibrary()
        dl.winappdriver.process = MagicMock()
        dl.winappdriver.process.pid = 1
        psutil.Process.create_time = MagicMock()
        psutil.Process.children = MagicMock(return_value=[mock_child])
        self.assertFalse(dl.winappdriver.process is None)
        dl.driver_teardown()
        self.assertTrue(dl.winappdriver.process is None)

    def test_open_application_successful(self):
        dl = DesktopLibrary()
        webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url')
        self.assertTrue(dl._cache.current)

    def test_open_multiple_applications_successful(self):
        dl = DesktopLibrary()
        webdriver.Remote = WebdriverRemoteMock
        dl.open_application('remote_url', alias='App1')
        dl.open_application('remote_url', alias='App2', desktop_alias='Desktop2')
        dl.switch_application('Desktop')
        dl.switch_application('Desktop2')
        self.assertRaisesRegex(RuntimeError, "Non-existing index or alias 'Desktop3'.", dl.switch_application,
                               'Desktop3')

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

    def test_open_application_window_name_non_exact(self):
        dl = DesktopLibrary()
        subprocess.Popen = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_xpath = MagicMock()
        self.assertFalse(dl._cache.current)
        dl.open_application('remote_url', window_name='test', app='testApp', exact_match=False)
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
        webdriver.Remote.find_element_by_name = MagicMock()
        webdriver.Remote.find_element_by_name.side_effect = [WebDriverException, "Window", "Window"]
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

    def test_switch_application_failure_4(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_xpath = MagicMock(side_effect=[WebDriverException, MagicMock(), MagicMock()])
        dl.switch_application_by_name('remote_url', window_name='test', exact_match=False)

    def test_switch_application_by_locator_success(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_class_name = MagicMock(side_effect=[MagicMock()])
        dl.switch_application_by_locator('remote_url', locator='class=test')
        self.assertTrue(dl._cache.current)

    def test_switch_application_by_locator_success_2(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_class_name = MagicMock(WebDriverException, MagicMock(), MagicMock())
        dl.switch_application_by_locator('remote_url', locator='class=test')
        self.assertTrue(dl._cache.current)

    def test_switch_application_by_locator_success_3(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_name = MagicMock(side_effect=[MagicMock()])
        dl.switch_application_by_locator('remote_url', name='test', app='some_app')
        self.assertTrue(dl._cache.current)

    def test_switch_application_by_locator_failure(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_class_name = MagicMock(side_effect=[WebDriverException, WebDriverException])
        self.assertRaisesRegex(AssertionError, 'Error finding window "class=test" in the desktop session. Is it a top level '
                                               'window handle?.', dl.switch_application_by_locator,
                                               'remote_url', locator='class=test')

    def test_switch_application_by_locator_failure_2(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        webdriver.Remote = WebdriverRemoteMock
        webdriver.Remote.find_element_by_name = MagicMock()
        webdriver.Remote.find_element_by_name.side_effect = [WebDriverException, MagicMock(), WebDriverException]
        self.assertRaisesRegex(AssertionError, 'Error finding window "name=test" in the desktop session. Is it a top level '
                                               'window handle?.', dl.switch_application_by_locator,
                                               'remote_url', locator='name=test')

    def test_switch_application_by_locator_failure_3(self):
        dl = DesktopLibrary()
        dl._run_on_failure = MagicMock()
        web_driver_mock = WebdriverRemoteMock
        webdriver.Remote = MagicMock(side_effect=[web_driver_mock, Exception])
        web_driver_mock.find_element_by_xpath = MagicMock()
        web_driver_mock.quit = MagicMock(return_value=True)
        self.assertRaisesRegex(AssertionError, 'Error connecting webdriver to window "xpath=//test".',
                               dl.switch_application_by_locator, 'remote_url', locator='xpath=//test')

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
        mock_desk.current_element.clear.assert_called()

    def test_wait_for_and_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_click_element(mock_desk, "some_locator")
        mock_desk.current_element.click.assert_called()

    def test_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.click_element(mock_desk, "some_locator")
        mock_desk._element_find.assert_called_with("some_locator", True, True)

    def test_wait_for_and_input_password(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_input_password(mock_desk, "some_locator", "some_text")
        mock_desk.current_element.send_keys.assert_called_with("some_text")

    def test_wait_for_and_input_text(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_input_text(mock_desk, "some_locator", "some_text")
        mock_desk.current_element.send_keys.assert_called_with("some_text")

    @patch("appium.webdriver.common.touch_action.TouchAction.press")
    def test_wait_for_and_long_press(self, press):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_long_press(mock_desk, "some_locator", 1000)
        press.assert_called()

    def test_wait_until_element_contains(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_contains(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_contain_text.assert_called_with(unittest.mock.ANY, "test_text", None)

    def test_wait_until_element_does_not_contain(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_does_not_contain(mock_desk, "some_locator", 'test_text')
        mock_desk.element_should_not_contain_text.assert_called_with(unittest.mock.ANY, "test_text", None)

    def test_element_should_be_enabled(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=True)
        DesktopLibrary.element_should_be_enabled(mock_desk, "some_locator")
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_element_should_be_enabled_error(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=False)
        self.assertRaisesRegex(AssertionError, "Element 'some_locator' should be enabled but did "
                               "not", DesktopLibrary.element_should_be_enabled, mock_desk,
                               "some_locator")
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_element_should_be_enabled_current_element_set(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=True)
        DesktopLibrary.element_should_be_enabled(mock_desk, mock_desk.current_element)
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_element_should_be_disabled(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=False)
        DesktopLibrary.element_should_be_disabled(mock_desk, "some_locator")
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_element_should_be_disabled_error(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=True)
        self.assertRaisesRegex(AssertionError, "Element 'some_locator' should be disabled but did "
                               "not", DesktopLibrary.element_should_be_disabled, mock_desk,
                               "some_locator")
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_element_should_be_disabled_current_element_set(self):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        mock_desk._check_for_cached_element().is_enabled = MagicMock(return_value=False)
        DesktopLibrary.element_should_be_disabled(mock_desk, mock_desk.current_element)
        mock_desk._check_for_cached_element().is_enabled.assert_called_with()

    def test_wait_until_element_is_enabled(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_is_enabled(mock_desk, "some_locator")
        mock_desk.element_should_be_enabled.assert_called_with(unittest.mock.ANY)

    def test_wait_until_element_is_disabled(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_until_element_is_disabled(mock_desk, "some_locator")
        mock_desk.element_should_be_disabled.assert_called_with(unittest.mock.ANY)

    def test_mouse_over_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.mouse_over_element(mock_desk, "some_locator")
        mock_desk._move_to_element.assert_called_with(unittest.mock.ANY, unittest.mock.ANY, 0, 0)

    def test_mouse_over_element_current_element_set(self):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        DesktopLibrary.mouse_over_element(mock_desk, mock_desk.current_element)
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
        mock_desk.mouse_over_element.assert_called_with(unittest.mock.ANY, 0, 0)

    def test_wait_for_and_mouse_over_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_element.assert_called_with(unittest.mock.ANY, 100, 100)

    def test_wait_for_and_mouse_over_and_click_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator")
        mock_desk.mouse_over_and_click_element.assert_called_with(unittest.mock.ANY, False, 0, 0)

    def test_wait_for_and_mouse_over_and_click_element_with_offset(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator", x_offset=100, y_offset=100)
        mock_desk.mouse_over_and_click_element.assert_called_with(unittest.mock.ANY, False, 100, 100)

    def test_wait_for_and_mouse_over_and_click_element_with_double_click(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_mouse_over_and_click_element(mock_desk, "some_locator", double_click=True)
        mock_desk.mouse_over_and_click_element.assert_called_with(unittest.mock.ANY, True, 0, 0)

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

    def test_element_find_by_image(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        DesktopLibrary._element_find(mock_desk, "image='file.png", True, True)
        mock_desk._current_application().find_element_by_image.assert_called_with('file.png')

    def test_element_find_by_image_fail(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        mock_desk._current_application().find_element_by_image = \
            MagicMock(side_effect=InvalidSelectorException)
        self.assertRaisesRegex(AssertionError, 'Selecting by image is only available when using '
                               'Appium v1.18.0 or higher', DesktopLibrary._element_find, mock_desk,
                               'file.png', True, True)

    def test_elements_find_by_image(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        DesktopLibrary._element_find(mock_desk, "image='file.png", False, True)
        mock_desk._current_application().find_elements_by_image.assert_called_with('file.png')

    def test_elements_find_by_image_fail(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        mock_desk._current_application().find_elements_by_image = \
            MagicMock(side_effect=InvalidSelectorException)
        self.assertRaisesRegex(AssertionError, 'Selecting by image is only available when using '
                               'Appium v1.18.0 or higher', DesktopLibrary._element_find, mock_desk,
                               'file.png', False, True)

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

    def test_is_element_present_by_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['name', 'Capture'])
        DesktopLibrary._is_element_present(mock_desk, "Name='Capture'")
        mock_desk._current_application().find_elements_by_name.assert_called_with('Capture')

    def test_is_element_present_by_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['accessibility_id', 'Capture'])
        DesktopLibrary._is_element_present(mock_desk, "accessibility_id='Capture'")
        mock_desk._current_application().find_elements_by_accessibility_id.assert_called_with(
            'Capture')

    def test_is_element_present_by_class_name(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['class', 'Capture'])
        DesktopLibrary._is_element_present(mock_desk, "class='Capture'")
        mock_desk._current_application().find_elements_by_class_name.assert_called_with('Capture')

    def test_is_element_present_by_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['xpath', 'Capture'])
        DesktopLibrary._is_element_present(mock_desk, "xpath=//TreeItem[@Name='Capture']")
        mock_desk._current_application().find_elements_by_xpath.assert_called_with('Capture')

    def test_is_element_present_by_default_xpath(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "//TreeItem[@Name='Capture']"])
        DesktopLibrary._is_element_present(mock_desk, "//TreeItem[@Name='Capture']")
        mock_desk._current_application().find_elements_by_xpath.assert_called_with(
            "//TreeItem[@Name='Capture']")

    def test_is_element_present_by_default_accessibility_id(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=[None, "Capture"])
        DesktopLibrary._is_element_present(mock_desk, "Capture")
        mock_desk._current_application().find_elements_by_accessibility_id.assert_called_with(
            'Capture')

    def test_is_element_present_by_image(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        DesktopLibrary._is_element_present(mock_desk, "image='file.png")
        mock_desk._current_application().find_elements_by_image.assert_called_with('file.png')

    def test_is_element_present_by_image_fail(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['image', 'file.png'])
        mock_desk._current_application().find_elements_by_image = \
            MagicMock(side_effect=InvalidSelectorException)
        self.assertRaisesRegex(AssertionError, 'Selecting by image is only available when using '
                               'Appium v1.18.0 or higher', DesktopLibrary._is_element_present, mock_desk,
                               'file.png')

    def test_is_element_present_fail(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['blockbuster_id', '123456789'])
        self.assertRaisesRegex(AssertionError,
                               "Element locator with prefix 'blockbuster_id' is not supported",
                               DesktopLibrary._is_element_present, mock_desk,
                               "blockbuster_id=123456789")

    def test_is_element_present_list_greater_than_0(self):
        mock_desk = MagicMock()
        mock_desk._parse_locator = MagicMock(return_value=['name', 'Capture'])
        mock_desk._current_application().find_elements_by_name = \
            MagicMock(return_value=[MagicMock(), MagicMock()])
        DesktopLibrary._is_element_present(mock_desk, "Name='Capture'")
        mock_desk._current_application().find_elements_by_name.assert_called_with('Capture')

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

    def test_select_elements_from_menu_retry_desktop(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[True, NoSuchElementException, True])
        DesktopLibrary.select_elements_from_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_menu_retry_desktop_2(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[True, NoSuchElementException, NoSuchElementException, True])
        DesktopLibrary.select_elements_from_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_menu_no_desktop(self):
        mock_desk = MagicMock()
        DesktopLibrary.select_elements_from_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_context_menu_retry_desktop(self):
        mock_desk = MagicMock()
        mock_desk.mouse_over_and_context_click_element = MagicMock(side_effect=[NoSuchElementException, True, True])
        DesktopLibrary.select_elements_from_context_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.mouse_over_and_context_click('some_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_context_menu_retry_desktop_2(self):
        mock_desk = MagicMock()
        mock_desk.mouse_over_and_context_click_element = MagicMock(side_effect=[NoSuchElementException, NoSuchElementException, True, True])
        DesktopLibrary.select_elements_from_context_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.mouse_over_and_context_click('some_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_context_menu_retry_desktop_3(self):
        mock_desk = MagicMock()
        mock_desk.click_element = MagicMock(side_effect=[NoSuchElementException, NoSuchElementException, True, True])
        DesktopLibrary.select_elements_from_context_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.mouse_over_and_context_click('some_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_select_elements_from_context_menu_no_desktop(self):
        mock_desk = MagicMock()
        DesktopLibrary.select_elements_from_context_menu(mock_desk, 'some_locator', 'another_locator')
        mock_desk.click_element.mouse_over_and_context_click('some_locator')
        mock_desk.click_element.assert_called_with('another_locator')

    def test_wait_until_page_contains_private(self):
        mock_desk = MagicMock()
        DesktopLibrary._wait_until_page_contains(mock_desk, 'some_text', 5)
        mock_desk._wait_until.asser_called_with('some_text', 5)

    def test_wait_until_page_contains_element_private(self):
        mock_desk = MagicMock()
        DesktopLibrary._wait_until_page_contains_element(mock_desk, 'some_element', 5)
        mock_desk._wait_until.assert_called_with(5, "Element 'some_element' did not appear in "
                                                 "<TIMEOUT>", unittest.mock.ANY, 'some_element')

    def test_wait_until_no_error_timeout(self):
        mock_desk = MagicMock()
        self.assertRaisesRegex(AssertionError,
                               'Error', DesktopLibrary._wait_until_no_error, mock_desk,
                               1, _long_running_function)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.flick")
    def test_flick(self, flick):
        mock_desk = MagicMock()
        DesktopLibrary.flick(mock_desk, 50, 100)
        flick.assert_called_with(50, 100)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.flick_element")
    def test_flick_from_element(self, flick_element):
        mock_desk = MagicMock()
        DesktopLibrary.flick_from_element(mock_desk, "some_locator", 50, 100, 10)
        flick_element.assert_called_with(unittest.mock.ANY, 50, 100, 10)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.flick_element")
    def test_flick_from_element_current_element_set(self, flick_element):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        DesktopLibrary.flick_from_element(mock_desk, mock_desk.current_element, 50, 100, 10)
        flick_element.assert_called_with(unittest.mock.ANY, 50, 100, 10)

    def test_wait_for_and_flick_from_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_flick_from_element(mock_desk, "some_locator", 50, 100, 10)
        mock_desk.flick_from_element.assert_called_with(unittest.mock.ANY, 50, 100, 10)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.scroll")
    def test_scroll(self, scroll):
        mock_desk = MagicMock()
        DesktopLibrary.scroll(mock_desk, 50, 100)
        scroll.assert_called_with(50, 100)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.scroll_from_element")
    def test_scroll_from_element(self, scroll_from_element):
        mock_desk = MagicMock()
        DesktopLibrary.scroll_from_element(mock_desk, "some_locator", 50, 100)
        scroll_from_element.assert_called_with(unittest.mock.ANY, 50, 100)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.scroll_from_element")
    def test_scroll_from_element_current_element_set(self, scroll_from_element):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        DesktopLibrary.scroll_from_element(mock_desk, mock_desk.current_element, 50, 100)
        scroll_from_element.assert_called_with(unittest.mock.ANY, 50, 100)

    def test_wait_for_and_scroll_from_element(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_scroll_from_element(mock_desk, "some_locator", 50, 100)
        mock_desk.scroll_from_element.assert_called_with(unittest.mock.ANY, 50, 100)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.double_tap")
    def test_double_tap(self, double_tap):
        mock_desk = MagicMock()
        DesktopLibrary.double_tap(mock_desk,  "some_locator")
        double_tap.assert_called_with(unittest.mock.ANY)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.double_tap")
    def test_double_tap_current_element_set(self, double_tap):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        DesktopLibrary.double_tap(mock_desk, mock_desk.current_element)
        double_tap.assert_called_with(unittest.mock.ANY)

    @patch("appium.webdriver.common.touch_action.TouchAction.tap")
    def test_wait_for_and_tap(self, tap):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_tap(mock_desk, "some_locator")
        tap.assert_called_with(unittest.mock.ANY)

    def test_wait_for_and_double_tap(self):
        mock_desk = MagicMock()
        DesktopLibrary.wait_for_and_double_tap(mock_desk, "some_locator")
        mock_desk.double_tap.assert_called_with(unittest.mock.ANY)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.tap_and_hold")
    def test_drag_and_drop_by_touch(self, tap_and_hold):
        mock_desk = MagicMock()
        DesktopLibrary.drag_and_drop_by_touch(mock_desk, "some_locator", "some_other_locator")
        tap_and_hold.assert_called_with(unittest.mock.ANY, unittest.mock.ANY)

    @patch("selenium.webdriver.common.touch_actions.TouchActions.tap_and_hold")
    def test_drag_and_drop_by_touch_offset(self, tap_and_hold):
        mock_desk = MagicMock()
        DesktopLibrary.drag_and_drop_by_touch_offset(mock_desk, "some_locator", 50, 100)
        tap_and_hold.assert_called_with(unittest.mock.ANY, unittest.mock.ANY)

    def test_start_screen_recording(self):
        mock_desk = MagicMock()
        mock_desk._recording = None
        DesktopLibrary.start_screen_recording(mock_desk)
        self.assertTrue(mock_desk._recording == unittest.mock.ANY)

    def test_stop_screen_recording(self):
        mock_desk = MagicMock()
        mock_desk._recording = None
        DesktopLibrary.start_screen_recording(mock_desk)
        file = DesktopLibrary.stop_screen_recording(mock_desk)
        self.assertTrue(file == unittest.mock.ANY)

    def test_save_recording(self):
        mock_desk = MagicMock()
        mock_desk._recording = b'some data'
        mock_desk._is_remotepath_set = MagicMock(return_value=False)
        options = ["username=test"]
        mock_desk._get_screenrecord_paths = MagicMock(return_value=("path", "link"))
        file = DesktopLibrary._save_recording(mock_desk, "filename", options)
        self.assertTrue(file == "path")
        os.remove("path")

    def test_get_text(self):
        mock_desk = MagicMock()
        mock_desk.current_element = None
        DesktopLibrary._get_text(mock_desk, 1)
        mock_desk._check_for_cached_element.assert_called_with(1)

    def test_get_text_current_element_set(self):
        mock_desk = MagicMock()
        mock_desk.current_element = MagicMock()
        DesktopLibrary._get_text(mock_desk, mock_desk.current_element)
        mock_desk._element_find.assert_not_called()

    def test_get_text_element_none(self):
        mock_desk = MagicMock()
        mock_desk._check_for_cached_element = MagicMock(return_value=None)
        result = DesktopLibrary._get_text(mock_desk, mock_desk.current_element)
        self.assertEqual(result, None)

    def test_check_for_cached_element_true(self):
        mock_desk = MagicMock()
        mock_desk.current_element = "a locator"
        result = DesktopLibrary._check_for_cached_element(mock_desk, "a locator")
        self.assertEqual(result, "a locator")

    def test_check_for_cached_element_false(self):
        mock_desk = MagicMock()
        DesktopLibrary._check_for_cached_element(mock_desk, "a locator")
        mock_desk._element_find.assert_called_with("a locator", True, True)
