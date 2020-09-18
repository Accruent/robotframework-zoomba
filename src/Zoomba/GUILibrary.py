import itertools
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from robot.libraries.Collections import Collections
from time import time
from robot.utils import is_string
import importlib

# Importing ReactSelect
try:
    RS = importlib.import_module('Helpers.ReactSelect', package='Helpers')
except ModuleNotFoundError:
    RS = importlib.import_module('.Helpers.ReactSelect', package='Zoomba')


zoomba = BuiltIn()
zoomba_collections = Collections()

SCREENSHOT_COUNTER = itertools.count()

class GUILibrary(SeleniumLibrary):
    """Zoomba GUI Library

    This class inherits from the SeleniumLibrary Class, and expands it with some commonly used keywords. For more information on SeleniumLibrary please visit: https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
    """

    def __init__(self, timeout=5.0, implicit_wait=0.0, run_on_failure='Save Selenium Screenshot',
                 screenshot_root_directory=None, plugins=None, event_firing_webdriver=None):
        """GUILibrary can be imported with several optional arguments.

        - ``timeout``:
          Default value for `timeouts` used with ``Wait ...`` keywords.
        - ``implicit_wait``:
          Default value for `implicit wait` used when locating elements.
        - ``run_on_failure``:
          Default action for the `run-on-failure functionality`.
        - ``screenshot_root_directory``:
          Path to folder where possible screenshots are created or EMBED.
          See `Set Screenshot Directory` keyword for further details about EMBED.
          If not given, the directory where the log file is written is used.
        - ``plugins``:
          Allows extending the GUILibrary with external Python classes.
        - ``event_firing_webdriver``:
          Class for wrapping Selenium with
          [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver]
        """
        super().__init__(timeout, implicit_wait, run_on_failure, screenshot_root_directory, plugins,
                         event_firing_webdriver)

    @keyword("Element Value Should Be Equal")
    def element_value_should_be_equal(self, locator, expected_value):
        """Assert that the value attribute of a web element is equal to a given value\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        expected_value: (string) A string or int value to be compared against the actual web element value
        """
        value = self.get_value(locator)
        zoomba.should_be_equal(value, expected_value)

    @keyword("Element Value Should Not Be Equal")
    def element_value_should_not_be_equal(self, locator, expected_value):
        """Assert that the value attribute of a web element is not equal to a given value\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        expected_value: (string) A string or int value to be compared against the actual web element value
        """
        value = self.get_value(locator)
        zoomba.should_not_be_equal(value, expected_value)

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that tries to find a web element first, and then clicks it.
        If the element fails to be clicked, it will scroll to the bottom of the page and try again.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.click_element(locator)

    @keyword('Wait For And Input Text')
    def wait_for_and_input_text(self, locator, text, timeout=None):
        """This is a series of chained Selenium keywords, that tries to find a web element first, and then input text.
        If the element fails to typed into, it will scroll to the bottom of the page and try again.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        text: (string) Text to be typed into the input field.
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.input_text(locator, text)

    @keyword("Wait For And Select Frame")
    def wait_for_and_select_frame(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first waits until an iFrame exists in the page, and then
        selects it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_until_page_contains_element(locator, timeout)
        self.select_frame(locator)

    @keyword("Select Nested Frame")
    def select_nested_frame(self, *locators):
        """Selects a frame nested in other frames

        locators: (list) A list of selenium locators(CSS, XPATH, ID, NAME, etc)

        Example (Selects iframe3 after traversing iframe1 and iframe2):
        |  `Select Nested Frame`  |  id-iframe1  |  id=iframe2  |  id=iframe3  |
        """
        for locator in locators:
            self.wait_until_page_contains_element(locator)
            self.select_frame(locator)

    @keyword("Unselect and Select Frame")
    def unselect_and_select_frame(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first unselects the current iFrame, then executes a
        wait for and select frame for a new iFrame.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.unselect_frame()
        self.wait_for_and_select_frame(locator, timeout)

    @keyword("Wait For And Select From List")
    def wait_for_and_select_from_list(self, locator, target, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s).\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.select_from_list_by_label(locator, target)

    @keyword("Wait For And Select From List By Value")
    def wait_for_and_select_from_list_by_value(self, locator, target, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s) for it using the value attribute of the item(s) web element.\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.select_from_list_by_value(locator, target)

    @keyword("Wait For And Select From List By Index")
    def wait_for_and_select_from_list_by_index(self, locator, target, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s) for it using the index of the item(s) web element.\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.select_from_list_by_index(locator, target)

    @keyword("Wait For And Mouse Over")
    def wait_for_and_mouse_over(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, then executes a
        mouse over command on it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.mouse_over(locator)

    @keyword("Wait For And Select Checkbox")
    def wait_for_and_select_checkbox(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, then selects it
        if it's a checkbox.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.select_checkbox(locator)

    @keyword("Wait For And Mouse Over And Click")
    def wait_for_and_mouse_over_and_click(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, executes a
        mouse over command on it, and it finally clicks it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_for_and_focus_on_element(locator, timeout)
        self.mouse_over(locator)
        self.click_element(locator)

    @keyword("Wait For and Focus On Element")
    def wait_for_and_focus_on_element(self, locator, timeout=None):
        """This is a series of chained Selenium keywords, that first waits for an element to be on the DOM, executes
        Focus on it, then it waits for it to be visible.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        if not timeout:
            timeout = self.timeout
        self.wait_until_page_contains_element(locator, timeout)
        self.wait_until_element_is_visible(locator, timeout)
        zoomba.wait_until_keyword_succeeds(timeout, 1, "Set Focus To Element", locator)

    @keyword("Wait Until Window Opens")
    def wait_until_window_opens(self, title, timeout=None):
        """Used to get the titles of the current browser windows, then verify that the provided window title
        is among them.\n
        title: (string) The title of the window you are waiting for.\n
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        if timeout:
            timeout = time() + float(timeout)
        else:
            timeout = time() + self.timeout
        while time() < timeout:
            titles = self.get_window_titles()
            if title in titles:
                return
        zoomba.fail("Window with the title: '" + title + "' not found.")

    @keyword("Window Should Not Be Open")
    def window_should_not_be_open(self, title):
        """This is a series of chained Selenium keywords, used to check that a window with the title no longer exists.\n
        title: (string) The title of the window you are expecting to be closed.
        """
        titles = self.get_window_titles()
        zoomba_collections.list_should_not_contain_value(titles, title)

    @keyword("Wait For And Select Window")
    def wait_for_and_select_window(self, title, timeout=None):
        """This is a series of chained Selenium keywords, used to wait until a window with the title argument exists,
        then it selects that window.\n
        title: (string) The title of the window you are waiting for.
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        self.wait_until_window_opens(title, timeout)
        self.switch_window(title)

    @keyword("Scroll To Bottom Of Page")
    def scroll_to_bottom_of_page(self):
        """This keyword scrolls down to the bottom of the page, if jquery is not available it will scroll 20000 pixels

        """
        try:
            height = self.execute_javascript("return window.outerHeight")
        except BaseException as ex:  # lgtm [py/catch-base-exception]
            if ex:
                height = 20000
        self.execute_javascript(f"window.scrollTo(0,{height})")

    @keyword("Wait Until Javascript Is Complete")
    def wait_until_javascript_is_complete(self):
        """This keyword polls the jQuery.active flag, to track execution of AJAX requests. The web application needs
        to have jQuery in order for this to work.

        """
        for each in range(1, 20):
            jquery_started = self.execute_javascript("return jQuery.active==1")
            if jquery_started:
                break
        for each in range(1, 50):
            jquery_completed = self.execute_javascript("return window.jQuery!=undefined && jQuery.active==0")
            if jquery_completed:
                break
            zoomba.sleep("0.5s")

    @keyword("Get Text From Web Elements List")
    def get_text_from_web_elements_list(self, web_elements_list):
        """This keyword extracts the HTML text of a list of web elements, and returns a list.\n
        web_elements_list: (array of selenium web elements) A selenium web element objects list.\n
        return: (array of strings) A list of strings extracted from the web elements.
        """
        text_element_list = []
        for web_element in web_elements_list:
            element_text = self.get_text(web_element)
            text_element_list.append(element_text)
        return text_element_list

    @keyword("Get Values From Web Elements List")
    def get_values_from_web_elements_list(self, web_elements_list):
        """This keyword extracts the HTML value of a list of web elements, and returns a list.\n
        web_elements_list: (array of selenium web elements) A selenium web element objects list.\n
        return: (array of strings) A list of strings extracted from the web elements.
        """
        value_element_list = []
        for web_element in web_elements_list:
            element_value = self.get_value(web_element)
            value_element_list.append(element_value)
        return value_element_list

    @keyword("Get Vertical Position From Web Elements List")
    def get_vertical_position_from_web_elements_list(self, web_elements_list):
        """This keyword extracts the vertical position in pixels of a list of web elements, and returns a list.\n
        web_elements_list: (array of selenium web elements) A selenium web element objects list.\n
        return: (array of integers) A list of integers of the vertical pixel positions for the provided web elements.
        """
        position_element_list = []
        for web_element in web_elements_list:
            element_position = self.get_vertical_position(web_element)
            position_element_list.append(element_position)
        return position_element_list

    @keyword("Wait Until Window Closes")
    def wait_until_window_closes(self, title, timeout=None):
        """This is a series of chained Selenium keywords, used to wait until a window with the title no longer exists.\n
        title: (string) The title of the window you are expecting to close.
        timeout: (float) Time in seconds to wait, will use global timeout if not set.
        """
        if not timeout:
            timeout = self.timeout
        zoomba.wait_until_keyword_succeeds(timeout, 1, "Window Should Not Be Open", title)

    @keyword("Wait Until Element Contains Value")
    def wait_until_element_contains_value(self, locator, expected_value, timeout=None):
        """Waits until the element ``locator`` appears on the current page and contains value.
        Fails if ``timeout`` expires before the element appears. See
        the `Timeouts` section for more information about using timeouts and
        their default value and the `Locating elements` section for details
        about the locator syntax.
        """
        self.wait_until_page_contains_element(locator, timeout)
        value = self.get_value(locator)
        zoomba.should_contain(value, expected_value)

    @keyword("Create Dictionary From Keys And Values Lists")
    def create_dictionary_from_keys_and_values_lists(self, keys, values):
        """This keyword returns a dictionary, given a list of keys and a list of values of the same length.\n
        keys: (array of strings) A list of keys to be assigned to a dictionary.\n
        values: (array of strings,integers,dictionaries,etc) A list of values to be assigned to a dictionary.\n
        return: (dictionary) A dictionary with the mapped key-value pairs.
        """
        if len(keys) != len(values):
            zoomba.log("The length of the keys and values lists is not the same: \nKeys Length: " +
                       str(len(keys)) + "\nValues Length: " + str(len(values)), "ERROR")
        new_dict = dict(zip(keys, values))
        return new_dict

    @keyword("Truncate String")
    def truncate_string(self, string, number_of_characters):
        """Truncates a given string to a certain amount of the given number of characters parameter.\n
        string: (string) Original String
        number_of_characters: (integer) Truncation index
        return: (string) A truncated String
        """
        truncated_string = string[0:number_of_characters]
        return truncated_string

    @keyword("Save Selenium Screenshot")
    def save_selenium_screenshot(self):
        """Takes a screenshot with a unique filename to be stored in Robot Framework compiled reports.

        If `Set Screenshot Directory` has been set to ``EMBED`` then the screenshot will be embedded into the report
        """
        if is_string(self.screenshot_root_directory):
            if self.screenshot_root_directory.upper() == 'EMBED':
                return self.capture_page_screenshot()
        else:
            timestamp = time()
            filename = 'selenium-screenshot-' + str(timestamp) + '-' + str(next(SCREENSHOT_COUNTER)) + '.png'
            return self.capture_page_screenshot(filename)

    @keyword("Get Element CSS Attribute Value")
    def get_element_css_attribute_value(self, locator, attribute):
        """Get the CSS attribute value of an element. This would be the values within the 'style' tag.

        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)

        attribute: (string) The attribute you wish to get the value for.
        """
        css = self.get_webelement(locator)
        attribute_value = zoomba.call_method(css, 'value_of_css_property', attribute)
        return attribute_value

    @keyword("Element CSS Attribute Value Should Be")
    def element_css_attribute_value_should_be(self, locator, attribute, expected_value):
        """Get the CSS attribute value of an element and compare it to an expected value.
        This would be the values within the 'style' tag.

        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)

        attribute: (string) The attribute you wish to get the value for.

        expected_value: (string) The expected attribute value to be compared against the actual
        attribute value
        """
        attribute_value = self.get_element_css_attribute_value(locator, attribute)
        zoomba.should_be_equal(attribute_value, expected_value)

    @keyword("Get React List Labels")
    def get_react_list_labels(self, locator):
        """This keyword grabs the labels from a React-Select list. See https://react-select.com/home for
        more information on React-Select components.

        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)

        """
        react_select_container = self.find_element(locator)
        options = RS.ReactSelect(react_select_container).options()
        return [opt.text for opt in options]
