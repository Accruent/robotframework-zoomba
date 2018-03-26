import os
import sys
sys.path.insert(0, os.path.abspath( os.path.join(os.path.dirname(__file__), '../../src/') ))

from Zoomba.GUILibrary import GUILibrary
import unittest
from unittest.mock import patch
from unittest.mock import Mock


class TestInternal(unittest.TestCase):
    @patch('robot.libraries.BuiltIn.BuiltIn.should_be_equal')
    def test_should_be_equal_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_value = Mock(return_value="expected_value")
        GUILibrary.element_value_should_be_equal(mock_gui, "some_locator", "expected_value")
        assert robot_call.called_with("expected_value", "expected_value")

    @patch('robot.libraries.BuiltIn.BuiltIn.should_not_be_equal')
    def test_should_not_be_equal_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_value = Mock(return_value="other_value")
        GUILibrary.element_value_should_not_be_equal(mock_gui, "some_locator", "expected_value")
        assert robot_call.called_with("other_value", "expected_value")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_for_and_focus_simple(self, robot_call):
        mock_gui = Mock()
        GUILibrary.wait_for_and_focus_on_element(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.ElementKeywords.click_element')
    def test_wait_for_and_click_element_simple(self, robot_call, click_element):
        mock_gui = Mock()
        GUILibrary.wait_for_and_click_element(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert click_element.called_with("some_locator")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.FormElementKeywords.input_text')
    def test_wait_for_and_input_text_simple(self, robot_call, input_text):
        mock_gui = Mock()
        GUILibrary.wait_for_and_input_text(mock_gui, "some_locator", "text")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert input_text.called_with("some_locator", "text")
        
    @patch('SeleniumLibrary.WaitingKeywords.wait_until_page_contains_element')
    @patch('SeleniumLibrary.FrameKeywords.select_frame')
    def test_wait_for_and_select_frame_simple(self, robot_call, select_frame):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_frame(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_frame.called_with("some_locator")

    @patch('SeleniumLibrary.WaitingKeywords.wait_until_page_contains_element')
    @patch('SeleniumLibrary.FrameKeywords.select_frame')
    def test_unselect_and_select_frame_simple(self, select_frame, robot_call):
        mock_gui = Mock()
        GUILibrary.unselect_and_select_frame(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_frame.called_with("some_locator")
        assert mock_gui.unselect_frame.called

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.SelectElementKeywords.select_from_list_by_label')
    def test_wait_for_and_select_from_list_simple(self, robot_call, select_list):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list(mock_gui, "some_locator", "target")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_list.called_with("some_locator", "target")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.SelectElementKeywords.select_from_list_by_value')
    def test_wait_for_and_select_from_list_by_value_simple(self, robot_call, select_list):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_value(mock_gui, "some_locator", "target")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_list.called_with("some_locator", "target")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.SelectElementKeywords.select_from_list_by_index')
    def test_wait_for_and_select_from_list_by_index_simple(self, robot_call, select_list):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_from_list_by_index(mock_gui, "some_locator", "target")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_list.called_with("some_locator", "target")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.ElementKeywords.mouse_over')
    def test_wait_for_mouse_over_simple(self, robot_call, mouse_over):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert mouse_over.called_with("some_locator")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.ElementKeywords.mouse_over')
    @patch('SeleniumLibrary.ElementKeywords.click_element')
    def test_wait_for_mouse_over_and_click_simple(self, robot_call, mouse_over, click_element):
        mock_gui = Mock()
        GUILibrary.wait_for_and_mouse_over_and_click(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert mouse_over.called_with("some_locator")
        assert click_element.called_with("some_locator")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.FormElementKeywords.select_checkbox')
    def test_wait_for_and_select_checkbox_simple(self, robot_call, select_checkbox):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_checkbox(mock_gui, "some_locator")
        assert robot_call.called_with(15, 1, "Set Focus To Element", "some_locator")
        assert select_checkbox.called_with("some_locator")

    @patch('robot.libraries.Collections.Collections.list_should_contain_value')
    def test_wait_until_window_opens_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_window_titles = Mock(return_value=["title"])
        GUILibrary.wait_until_window_opens(mock_gui, "title")
        assert robot_call.called_with(["title"], "title")

    @patch('robot.libraries.Collections.Collections.list_should_not_contain_value')
    def test_window_should_not_be_open_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_window_titles = Mock(return_value=["main"])
        GUILibrary.window_should_not_be_open(mock_gui, "title")
        assert robot_call.called_with(["main"], "title")

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    @patch('SeleniumLibrary.WindowKeywords.select_window')
    def test_wait_for_and_select_window_simple(self, robot_call, select_window):
        mock_gui = Mock()
        GUILibrary.wait_for_and_select_window(mock_gui, "title")
        assert robot_call.called_with(15, 1, "wait_until_window_opens", "title")
        assert select_window.called_with("title")

    @patch('robot.libraries.BuiltIn.BuiltIn.sleep')
    def test_wait_until_javascript_is_complete_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.execute_javascript = Mock(side_effect=[False, True, False, True])
        GUILibrary.wait_until_javascript_is_complete(mock_gui)
        assert robot_call.called

    @patch('SeleniumLibrary.ElementKeywords.get_text')
    def test_get_text_from_web_elements_list_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_text = Mock(side_effect=['a', 'b'])
        assert GUILibrary.get_text_from_web_elements_list(mock_gui, ['a', 'b']) == ['a', 'b']

    @patch('SeleniumLibrary.ElementKeywords.get_value')
    def test_get_values_from_web_elements_list_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_value = Mock(side_effect=['a', 'b'])
        assert GUILibrary.get_values_from_web_elements_list(mock_gui, ['a', 'b']) == ['a', 'b']

    @patch('SeleniumLibrary.ElementKeywords.get_vertical_position')
    def test_get_vertical_position_from_web_elements_list_simple(self, robot_call):
        mock_gui = Mock()
        mock_gui.get_vertical_position = Mock(side_effect=[1, 2])
        assert GUILibrary.get_vertical_position_from_web_elements_list(mock_gui, ['a', 'b']) == [1, 2]

    @patch('robot.libraries.BuiltIn.BuiltIn.wait_until_keyword_succeeds')
    def test_wait_until_window_closes_simple(self, robot_call):
        mock_gui = Mock()
        GUILibrary.wait_until_window_closes(mock_gui, "title")
        assert robot_call.called_with(15, 1, "Window Should Not Be Open", "title")

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
        assert GUILibrary.create_dictionary_from_keys_and_values_lists(mock_gui, [5], [6]) == {5:6}

    @patch('robot.libraries.BuiltIn.BuiltIn.log')
    def test_create_dictionary_from_keys_and_values_lists_fail(self, robot_call):
        mock_gui = Mock()
        GUILibrary.create_dictionary_from_keys_and_values_lists(mock_gui, [5], [6, 7])
        assert robot_call.called_with("The length of the keys and values lists is not the same: \nKeys Length: " +
                             "1" + "\nValues Length: " + "2", "ERROR")

    def test_truncate_string_simple(self):
        mock_gui = Mock()
        assert GUILibrary.truncate_string(mock_gui, "string", 3) == "str"

    def test_drag_and_drop_by_js_simple(self):
        mock_gui = Mock()
        GUILibrary.drag_and_drop_by_js(mock_gui, "source", "target", True)
        mock_gui.driver.execute_async_script.assert_called()
        mock_gui.driver.execute_script.assert_called()

    def test_drag_and_drop_by_js_false(self):
        mock_gui = Mock()
        GUILibrary.drag_and_drop_by_js(mock_gui, "source", "target", False)
        mock_gui.driver.execute_async_script.assert_not_called()
        mock_gui.driver.execute_script.assert_called()

    @patch('robot.libraries.BuiltIn.BuiltIn.log')
    def test_scroll_element_into_view_fail(self, robot_call):
        mock_gui = Mock()
        mock_gui.find_element.return_value = "found it!"
        GUILibrary.scroll_element_into_view(mock_gui, "locator")
        robot_call.assert_called_with("Scrolling element 'locator' into view.", level='INFO')
        mock_gui.find_element.assert_called_with(locator="locator")
        mock_gui.driver.execute_script.assert_called_with('arguments[0].scrollIntoView()', "found it!")

