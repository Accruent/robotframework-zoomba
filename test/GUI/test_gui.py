"""Unit tests for GUILibrary keywords"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock, Mock, PropertyMock
from Zoomba.GUILibrary import GUILibrary
from Zoomba.Helpers import ReactSelect
from selenium.common.exceptions import UnexpectedTagNameException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))


class TestInternal(unittest.TestCase):
    def test_import_defaults(self):
        GUILibrary()

    @patch('robot.libraries.BuiltIn.BuiltIn.should_be_equal')
    def test_should_be_equal_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_value = Mock(return_value="expected_value")
        GUILibrary.element_value_should_be_equal(mock_gui, "some_locator", "expected_value")
        robot_call.assert_called_with("expected_value", "expected_value")

    @patch('robot.libraries.BuiltIn.BuiltIn.should_not_be_equal')
    def test_should_not_be_equal_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_value = Mock(return_value="other_value")
        GUILibrary.element_value_should_not_be_equal(mock_gui, "some_locator", "expected_value")
        robot_call.assert_called_with("other_value", "expected_value")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_for_and_focus_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.timeout = 15
        GUILibrary.wait_for_and_focus_on_element(mock_gui, "some_locator")
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", 15)
        robot_call.assert_called_with(15, 1, "Set Focus To Element", "some_locator")
        mock_gui.wait_until_element_is_visible.assert_called_with("some_locator", 15)

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_for_and_focus_with_timeout_override(self, robot_call):
        mock_gui = Mock()
        mock_gui.timeout = 15
        GUILibrary.wait_for_and_focus_on_element(mock_gui, "some_locator", 10)
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", 10)
        robot_call.assert_called_with(10, 1, "Set Focus To Element", "some_locator")
        mock_gui.wait_until_element_is_visible.assert_called_with("some_locator", 10)

    def test_wait_for_and_click_element_simple(self):
        mock_gui = Mock()
        mock_gui.timeout = 10.5
        GUILibrary.wait_for_and_click_element(mock_gui, "some_locator")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.click_element.assert_called_with("some_locator")

    def test_wait_for_and_click_element_with_timeout(self):
        mock_gui = Mock()
        mock_gui.timeout = 15
        GUILibrary.wait_for_and_click_element(mock_gui, "some_locator", timeout=10.5)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 10.5)
        mock_gui.click_element.assert_called_with("some_locator")

    def test_wait_for_and_input_text_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_input_text(mock_gui, "some_locator", "text")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.input_text.assert_called_with("some_locator", "text")

    def test_wait_for_and_input_text_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_input_text(mock_gui, "some_locator", "text", 5)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 5)
        mock_gui.input_text.assert_called_with("some_locator", "text")

    def test_wait_for_and_input_password_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_input_password(mock_gui, "some_locator", "text")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.input_password.assert_called_with("some_locator", "text")

    def test_wait_for_and_input_password_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_input_password(mock_gui, "some_locator", "text", 5)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 5)
        mock_gui.input_password.assert_called_with("some_locator", "text")

    def test_wait_for_and_select_frame_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_frame(mock_gui, "some_locator")
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", None)
        mock_gui.select_frame.assert_called_with("some_locator")

    def test_wait_for_and_select_frame_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_frame(mock_gui, "some_locator", 5)
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", 5)
        mock_gui.select_frame.assert_called_with("some_locator")

    def test_unselect_and_select_frame_simple(self):
        mock_gui = Mock()
        GUILibrary.unselect_and_select_frame(mock_gui, "some_locator")
        mock_gui.wait_for_and_select_frame.assert_called_with("some_locator", None)
        mock_gui.unselect_frame.assert_called()

    def test_unselect_and_select_frame_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.unselect_and_select_frame(mock_gui, "some_locator", timeout=7.5)
        mock_gui.wait_for_and_select_frame.assert_called_with("some_locator", 7.5)
        mock_gui.unselect_frame.assert_called()

    def test_select_nested_frame(self):
        mock_gui = Mock()
        GUILibrary.select_nested_frame(mock_gui, "some_locator", "another_locator", "one_more")
        mock_gui.wait_until_page_contains_element.assert_called_with("one_more")
        mock_gui.select_frame.assert_called_with("one_more")

    def test_wait_for_and_select_from_list_simple(self):
        mock_gui = Mock()
        mock_gui.timeout = 12
        GUILibrary.wait_for_and_select_from_list(mock_gui, "some_locator", "target")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.select_from_list_by_label.assert_called_with("some_locator", "target")

    def test_wait_for_and_select_from_list_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list(mock_gui, "some_locator", "target", 10)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 10)
        mock_gui.select_from_list_by_label.assert_called_with("some_locator", "target")

    def test_wait_for_and_select_from_list_by_value_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_value(mock_gui, "some_locator", "target")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.select_from_list_by_value.assert_called_with("some_locator", "target")

    def test_wait_for_and_select_from_list_by_value_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_value(mock_gui, "some_locator", "target", 11)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 11)
        mock_gui.select_from_list_by_value.assert_called_with("some_locator", "target")

    def test_wait_for_and_select_from_list_by_index_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_index(mock_gui, "some_locator", "target")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.select_from_list_by_index.assert_called_with("some_locator", "target")

    def test_wait_for_and_select_from_list_by_index_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_index(mock_gui, "some_locator", "target", 5)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 5)
        mock_gui.select_from_list_by_index.assert_called_with("some_locator", "target")

    @patch("selenium.webdriver.common.action_chains.ActionChains.scroll_by_amount")
    def test_mouse_scroll_simple(self, scroll_by_amount):
        mock_gui = Mock()
        GUILibrary.mouse_scroll(mock_gui, 500, -100)
        scroll_by_amount.assert_called_with(500, -100)

    @patch("selenium.webdriver.common.action_chains.ActionChains.scroll_from_origin")
    @patch("selenium.webdriver.common.actions.wheel_input.ScrollOrigin")
    def test_mouse_scroll_over_element_simple(self, ScrollOrigin, scroll_from_origin):
        mock_gui = Mock()
        GUILibrary.mouse_scroll_over_element(mock_gui, "some_locator", 500, -100)
        scroll_from_origin.assert_called_with(unittest.mock.ANY, 500, -100)

    def test_wait_for_mouse_over_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over(mock_gui, "some_locator")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.mouse_over.assert_called_with("some_locator")

    def test_wait_for_mouse_over_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over(mock_gui, "some_locator", 12)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 12)
        mock_gui.mouse_over.assert_called_with("some_locator")

    def test_wait_for_mouse_over_and_click_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over_and_click(mock_gui, "some_locator")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.mouse_over.assert_called_with("some_locator")
        mock_gui.click_element.assert_called_with("some_locator")

    def test_wait_for_mouse_over_and_click_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over_and_click(mock_gui, "some_locator", 2)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 2)
        mock_gui.mouse_over.assert_called_with("some_locator")
        mock_gui.click_element.assert_called_with("some_locator")

    def test_wait_for_and_select_checkbox_simple(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_checkbox(mock_gui, "some_locator")
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", None)
        mock_gui.select_checkbox.assert_called_with("some_locator")

    def test_wait_for_and_select_checkbox_with_timeout(self):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_checkbox(mock_gui, "some_locator", 5)
        mock_gui.wait_for_and_focus_on_element.assert_called_with("some_locator", 5)
        mock_gui.select_checkbox.assert_called_with("some_locator")

    def test_wait_until_window_opens_simple(self):
        mock_gui = Mock()
        mock_gui.timeout = 10
        mock_gui.get_window_titles = Mock(return_value=["title"])
        GUILibrary.wait_until_window_opens(mock_gui, "title")
        mock_gui.get_window_titles.assert_called()

    def test_wait_until_window_opens_with_timeout(self):
        mock_gui = Mock()
        mock_gui.get_window_titles = Mock(return_value=["title"])
        GUILibrary.wait_until_window_opens(mock_gui, "title", 15)
        mock_gui.get_window_titles.assert_called()

    @patch('robot.libraries.BuiltIn.BuiltIn.fail')
    def test_wait_until_window_opens_with_error(self, fail):
        mock_gui = Mock()
        mock_gui.timeout = 0.0001
        mock_gui.get_window_titles = Mock(return_value=["wrong_title"])
        GUILibrary.wait_until_window_opens(mock_gui, "title")
        fail.assert_called_with("Window with the title: 'title' not found.")

    @patch('robot.libraries.Collections.Collections.list_should_not_contain_value')
    def test_window_should_not_be_open_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_window_titles = Mock(return_value=["main"])
        GUILibrary.window_should_not_be_open(mock_gui, "title")
        robot_call.assert_called_with(["main"], "title")

    def test_wait_for_and_select_window_simple(self):
        mock_gui = Mock()
        mock_gui.timeout = 15
        GUILibrary.wait_for_and_select_window(mock_gui, "title")
        mock_gui.wait_until_window_opens.assert_called_with("title", None)
        mock_gui.switch_window.assert_called_with("title")

    def test_wait_for_and_select_window_with_timeout(self):
        mock_gui = Mock()
        mock_gui.timeout = 15
        GUILibrary.wait_for_and_select_window(mock_gui, "title", 10)
        mock_gui.wait_until_window_opens.assert_called_with("title", 10)
        mock_gui.switch_window.assert_called_with("title")

    @patch('robot.libraries.BuiltIn.BuiltIn.sleep')
    def test_wait_until_javascript_is_complete(self, robot_call):
        mock_gui = Mock()
        mock_gui.execute_javascript = Mock(side_effect=["loading", False, "complete", False,
                                                        "complete", True, "complete", True])
        GUILibrary.wait_until_javascript_is_complete(mock_gui)
        robot_call.assert_called()

    @patch('robot.libraries.BuiltIn.BuiltIn.sleep')
    def test_wait_for_page_load(self, robot_call):
        mock_gui = Mock()
        mock_gui.execute_javascript = Mock(side_effect=["loading", "loading", "loading", "complete"])
        GUILibrary.wait_for_page_to_load(mock_gui)
        robot_call.assert_called()

    def test_get_text_from_web_elements_list_simple(self):
        mock_gui = Mock()
        mock_gui.get_text = Mock(side_effect=['a', 'b'])
        assert GUILibrary.get_text_from_web_elements_list(mock_gui, ['a', 'b']) == ['a', 'b']

    def test_get_values_from_web_elements_list_simple(self):
        mock_gui = Mock()
        mock_gui.get_value = Mock(side_effect=['a', 'b'])
        assert GUILibrary.get_values_from_web_elements_list(mock_gui, ['a', 'b']) == ['a', 'b']

    def test_get_vertical_position_from_web_elements_list_simple(self):
        mock_gui = Mock()
        mock_gui.get_vertical_position = Mock(side_effect=[1, 2])
        assert GUILibrary.get_vertical_position_from_web_elements_list(mock_gui, ['a', 'b']) == [1, 2]

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_until_window_closes_simple(self, robot_call):
        mock_gui = Mock()
        type(mock_gui).timeout = PropertyMock(return_value=15)
        GUILibrary.wait_until_window_closes(mock_gui, "title")
        robot_call.assert_called_with(15, 1, "Window Should Not Be Open", "title")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_until_window_closes_with_timeout(self, robot_call):
        mock_gui = Mock()
        type(mock_gui).timeout = PropertyMock(return_value=15)
        GUILibrary.wait_until_window_closes(mock_gui, "title", 6)
        robot_call.assert_called_with(6, 1, "Window Should Not Be Open", "title")

    def test_scroll_to_bottom_of_page_simple(self):
        mock_gui = Mock()
        mock_gui.execute_javascript = Mock(return_value=20)
        GUILibrary.scroll_to_bottom_of_page(mock_gui)
        mock_gui.execute_javascript.assert_called_with("window.scrollTo(0,20)")

    def test_scroll_to_bottom_of_page_exception(self):
        mock_gui = Mock()
        mock_gui.execute_javascript = Mock(side_effect=[BaseException, True])
        GUILibrary.scroll_to_bottom_of_page(mock_gui)
        mock_gui.execute_javascript.assert_called_with("window.scrollTo(0,20000)")

    def test_create_dictionary_from_keys_and_values_lists_simple(self):
        mock_gui = Mock()
        assert GUILibrary.create_dictionary_from_keys_and_values_lists(mock_gui, [5], [6]) == {5: 6}

    @patch('robot.libraries.BuiltIn.BuiltIn.log')
    def test_create_dictionary_from_keys_and_values_lists_fail(self, robot_call):
        mock_gui = Mock()
        GUILibrary.create_dictionary_from_keys_and_values_lists(mock_gui, [5], [6, 7])
        robot_call.assert_called_with("The length of the keys and values lists is not the same: \nKeys Length: " +
                                      "1" + "\nValues Length: " + "2", "ERROR")

    def test_truncate_string_simple(self):
        mock_gui = Mock()
        assert GUILibrary.truncate_string(mock_gui, "string", 3) == "str"

    @patch('SeleniumLibrary.ScreenshotKeywords.capture_page_screenshot')
    def test_save_selenium_screenshot_simple(self, mock_gui):
        GUILibrary.save_selenium_screenshot(mock_gui)
        mock_gui.capture_page_screenshot.assert_called_with(unittest.mock.ANY)

    @patch('SeleniumLibrary.ScreenshotKeywords.capture_page_screenshot')
    def test_save_selenium_screenshot_embed(self, mock_gui):
        mock_gui.screenshot_root_directory = 'EMBED'
        GUILibrary.save_selenium_screenshot(mock_gui)
        mock_gui.capture_page_screenshot.assert_called_with()

    @patch('robot.libraries.BuiltIn.BuiltIn.should_contain')
    def test_wait_until_element_contains_value_with_timeout(self, robot_call):
        mock_gui = Mock()
        GUILibrary.wait_until_element_contains_value(mock_gui, "some_locator", "expected_value", 5)
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", 5)
        mock_gui.get_value = Mock(return_value="expected_value")
        robot_call.assert_called()

    @patch('robot.libraries.BuiltIn.BuiltIn.should_contain')
    def test_wait_until_element_contains_value(self, robot_call):
        mock_gui = Mock()
        GUILibrary.wait_until_element_contains_value(mock_gui, "some_locator", "expected_value")
        mock_gui.wait_until_page_contains_element.assert_called_with("some_locator", None)
        mock_gui.get_value = Mock(return_value="expected_value")
        robot_call.assert_called()

    def test_get_element_css_attribute_value(self):
        mock_gui = Mock()
        mock_gui.get_webelement().value_of_css_property = Mock(return_value="some_attribute_value")
        value = GUILibrary.get_element_css_attribute_value(mock_gui, "some_locator", "some_attribute")
        self.assertEqual(value, "some_attribute_value")

    def test_element_css_attribute_value_should_be(self):
        mock_gui = Mock()
        mock_gui.get_element_css_attribute_value = Mock(return_value="some_attribute_value")
        GUILibrary.element_css_attribute_value_should_be(mock_gui, "some_locator", "some_attribute",
                                                         "some_attribute_value")

    def test_get_react_list_labels_simple(self):
        mock_gui = Mock()
        mock_webelement = Mock()
        mock_webelement.tag_name.lower = Mock(return_value='div')
        mock_gui.find_element = Mock(return_value=mock_webelement)
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.options') as mock_options:
            GUILibrary.get_react_list_labels(mock_gui, "some_locator")
            mock_gui.find_element.assert_called_with("some_locator")
            mock_options.assert_called()

    def test_get_react_list_labels_values(self):
        mock_gui = Mock()
        mock_webelement = Mock()
        mock_webelement.tag_name.lower = Mock(return_value='div')
        mock_option1 = Mock()
        mock_option1.text = 'option1'
        mock_option2 = Mock()
        mock_option2.text = 'option2'
        mock_gui.find_element = Mock(return_value=mock_webelement)
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.options', return_value=[mock_option1, mock_option2]):
            assert GUILibrary.get_react_list_labels(mock_gui, "some_locator") == ['option1', 'option2']

    def test_react_select_init(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        RS = ReactSelect.ReactSelect(mock_webelement)
        self.assertEqual(RS._el, mock_webelement)

    def test_react_select_init_tag_check(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'span'
        with self.assertRaises(UnexpectedTagNameException, msg="ReactSelect only works on <div> elements, not on <span>"):
            ReactSelect.ReactSelect(mock_webelement)

    def test_react_select_options_simple(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.expand_select_list') as mock_expand_select_list:
            ReactSelect.ReactSelect(mock_webelement).options()
            mock_expand_select_list.assert_called()

    def test_react_select_options(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        mock_webelement.find_elements = MagicMock(return_value=["some child element", "another child element"])
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.expand_select_list', return_value=True):
            assert ReactSelect.ReactSelect(mock_webelement).options() == ["some child element", "another child element"]

    def test_react_select_is_expanded(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        mock_webelement.find_elements = Mock(return_value=["some child element"])
        assert ReactSelect.ReactSelect(mock_webelement).is_expanded()

    def test_react_select_is_expanded_no_elements(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        mock_webelement.find_elements = Mock(return_value=[])
        assert not ReactSelect.ReactSelect(mock_webelement).is_expanded()

    def test_react_select_is_expanded_error(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        mock_webelement.find_elements = Mock(return_value=["some child element", "another child element"])
        with self.assertRaises(LookupError, msg="ReactSelect.is_expanded: Multiple selection menus found"):
            ReactSelect.ReactSelect(mock_webelement).is_expanded()

    def test_react_select_expand_select_list(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.is_expanded', return_value=False) as mock_is_expanded:
            ReactSelect.ReactSelect(mock_webelement).expand_select_list()
            mock_is_expanded.assert_called()
            mock_webelement.click.assert_called()

    def test_react_select_expand_select_list_already_expanded(self):
        mock_webelement = Mock()
        mock_webelement.tag_name = 'div'
        with patch('Zoomba.Helpers.ReactSelect.ReactSelect.is_expanded', return_value=True):
            ReactSelect.ReactSelect(mock_webelement).expand_select_list()
            mock_webelement.click.assert_not_called()
