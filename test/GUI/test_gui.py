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
        GUILibrary.wait_for_and_mouse_over(mock_gui, "some_locator")
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










