from SeleniumLibrary import SeleniumLibrary
from selenium.webdriver.remote.webelement import WebElement
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.Collections import Collections

zoomba = BuiltIn()
zoomba_collections = Collections()


class GUILibrary(SeleniumLibrary):
    """Zoomba GUI Library

    This class inherits from the Selenium2Library Class, and expands it with some commonly used keywords.
    """
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
    def wait_for_and_click_element(self, locator):
        """This is a series of chained Selenium keywords, that tries to find a web element first, and then clicks it.
        If the element fails to be clicked, it will scroll to the bottom of the page and try again.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_for_and_focus_on_element(locator)
        self.click_element(locator)

    @keyword('Wait For And Input Text')
    def wait_for_and_input_text(self, locator, text):
        """This is a series of chained Selenium keywords, that tries to find a web element first, and then input text.
        If the element fails to typed into, it will scroll to the bottom of the page and try again.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        text: (string) Text to be typed into the input field.
        """
        self.wait_for_and_focus_on_element(locator)
        self.input_text(locator, text)

    @keyword("Wait For And Select Frame")
    def wait_for_and_select_frame(self, locator):
        """This is a series of chained Selenium keywords, that first waits until an iFrame exists in the page, and then
        selects it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_until_page_contains_element(locator)
        self.select_frame(locator)

    @keyword("Unselect and Select Frame")
    def unselect_and_select_frame(self, locator):
        """This is a series of chained Selenium keywords, that first unselects the current iFrame, then executes a
        wait for and select frame for a new iFrame.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.unselect_frame()
        self.wait_for_and_select_frame(locator)

    @keyword("Wait For And Select From List")
    def wait_for_and_select_from_list(self, locator, target):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s).\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        """
        self.wait_for_and_focus_on_element(locator)
        self.select_from_list_by_label(locator, target)

    @keyword("Wait For And Select From List By Value")
    def wait_for_and_select_from_list_by_value(self, locator, target):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s) for it using the value attribute of the item(s) web element.\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        """
        self.wait_for_and_focus_on_element(locator)
        self.select_from_list_by_value(locator, target)

    @keyword("Wait For And Select From List By Index")
    def wait_for_and_select_from_list_by_index(self, locator, target):
        """This is a series of chained Selenium keywords, that first waits for and focuses on a list element, then
        selects an item(s) for it using the index of the item(s) web element.\n
        locator:  (string) A selenium locator(CSS, XPATH, ID, NAME, etc)\n
        target: (string, array of strings) The list item(s) to be selected (string, or list of strings)
        """
        self.wait_for_and_focus_on_element(locator)
        self.select_from_list_by_index(locator, target)

    @keyword("Wait For And Mouse Over")
    def wait_for_and_mouse_over(self, locator):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, then executes a
        mouse over command on it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_for_and_focus_on_element(locator)
        self.mouse_over(locator)

    @keyword("Wait For And Select Checkbox")
    def wait_for_and_select_checkbox(self, locator):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, then selects it
        if it's a checkbox.\n
        :locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_for_and_focus_on_element(locator)
        self.select_checkbox(locator)

    @keyword("Wait For And Mouse Over And Click")
    def wait_for_and_mouse_over_and_click(self, locator):
        """This is a series of chained Selenium keywords, that first waits for an element to be visible, executes a
        mouse over command on it, and it finally clicks it.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_for_and_focus_on_element(locator)
        self.mouse_over(locator)
        self.click_element(locator)

    @keyword("Wait For and Focus On Element")
    def wait_for_and_focus_on_element(self, locator):
        """This is a series of chained Selenium keywords, that first waits for an element to be on the DOM, executes
        Focus on it, then it waits for it to be visible.\n
        locator: (string) A selenium locator(CSS, XPATH, ID, NAME, etc)
        """
        self.wait_until_page_contains_element(locator)
        zoomba.wait_until_keyword_succeeds(self.timeout, 1, "Set Focus To Element", locator)
        self.wait_until_element_is_visible(locator)

    @keyword("Wait Until Window Opens")
    def wait_until_window_opens(self, title):
        """This is a series of chained Selenium keywords, used to get the titles of the current browser windows, then
        verify that the provided window title is among them.\n
        title: (string) The title of the window you are waiting for.
        """
        titles = self.get_window_titles()
        zoomba_collections.list_should_contain_value(titles, title)

    @keyword("Window Should Not Be Open")
    def window_should_not_be_open(self, title):
        """This is a series of chained Selenium keywords, used to check that a window with the title no longer exists.\n
        title: (string) The title of the window you are expecting to be closed.
        """
        titles = self.get_window_titles()
        zoomba_collections.list_should_not_contain_value(titles, title)

    @keyword("Wait For And Select Window")
    def wait_for_and_select_window(self, title):
        """This is a series of chained Selenium keywords, used to wait until a window with the title argument exists,
        then it selects that window.\n
        title: (string) The title of the window you are waiting for.
        """
        zoomba.wait_until_keyword_succeeds(self.timeout, 1, "Wait Until Window Opens", title)
        self.select_window(title)

    @keyword("Scroll To Bottom Of Page")
    def scroll_to_bottom_of_page(self):
        """This keyword scrolls down to the bottom of the page, if jquery is not available it will scroll 20000 pixels

        """
        try:
            height = self.execute_javascript("return window.outerHeight")
        except:
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
    def wait_until_window_closes(self, title):
        """This is a series of chained Selenium keywords, used to wait until a window with the title no longer exists.\n
        title: (string) The title of the window you are expecting to close.
        timeout: (integer) The amount of time (in seconds) the keyword will try to wait for the window to close.
        """
        zoomba.wait_until_keyword_succeeds(self.timeout, 1, "Window Should Not Be Open", title)

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

    @keyword("Drag And Drop By JS")
    def drag_and_drop_by_js(self, source, target, load_jquery=True):
        """Loads a JS helper function to simulate a drag and drop event. jQuery is necessary for the function to work.\n
        This method is a workaround for the Selenium 2 Library issue present in this issue:
        https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/3604

        source: (string) Source element to be given as xpath.\n
        target: (string) Target element to be given as xpath.\n
        load_jquery: (boolean) When set to True loads jQuery library onto the page via url.

        Examples:
        | Drag And Drop by JS | source | target | | # Move source over target. |
        | Drag And Drop by JS | source | target | False | # Move source over target. (No JQuery is loaded to the page) |
        """
        driver = self.driver
        driver.set_script_timeout(30)

        self.page_should_contain_element(source)
        self.page_should_contain_element(target)
        js = "(function( $ ) {$.fn.simulateDragDrop = function(options) {return this.each(function() {new $.simulateDragDrop(this, options); }); }; $.simulateDragDrop = function(elem, options) {this.options = options; this.simulateEvent(elem, options); }; $.extend($.simulateDragDrop.prototype, {simulateEvent: function(elem, options) {/*Simulating drag start*/ var type = 'dragstart'; var event = this.createEvent(type); this.dispatchEvent(elem, type, event); /*Simulating drop*/ type = 'drop'; var dropEvent = this.createEvent(type, {}); dropEvent.dataTransfer = event.dataTransfer; this.dispatchEvent($(options.dropTarget)[0], type, dropEvent); /*Simulating drag end*/ type = 'dragend'; var dragEndEvent = this.createEvent(type, {}); dragEndEvent.dataTransfer = event.dataTransfer; this.dispatchEvent(elem, type, dragEndEvent); }, createEvent: function(type) {var event = document.createEvent('CustomEvent'); event.initCustomEvent(type, true, true, null); event.dataTransfer = {data: {}, setData: function(type, val){this.data[type] = val; }, getData: function(type){return this.data[type]; } }; return event; }, dispatchEvent: function(elem, type, event) {if(elem.dispatchEvent) {elem.dispatchEvent(event); }else if( elem.fireEvent ) {elem.fireEvent('on'+type, event); } } }); })(jQuery);$(document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue) .simulateDragDrop({ dropTarget: document.evaluate(arguments[1], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue});"
        load_jquery_js = "/** dynamically load jQuery */ (function(jqueryUrl, callback) { if (typeof jqueryUrl != 'string') { jqueryUrl = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'; } if (typeof jQuery == 'undefined') { var script = document.createElement('script'); var head = document.getElementsByTagName('head')[0]; var done = false; script.onload = script.onreadystatechange = (function() { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) { done = true; script.onload = script.onreadystatechange = null; head.removeChild(script); callback(); } }); script.src = jqueryUrl; head.appendChild(script); } else { callback(); } })(arguments[0], arguments[arguments.length - 1]);"

        if load_jquery:
            driver.execute_async_script(load_jquery_js, None)
        driver.execute_script(js, source, target)

    @keyword("Scroll Element Into View")
    def scroll_element_into_view(self, locator):
        """Scrolls an element from given ``locator`` into view.
        Arguments:
        - ``locator``: The locator to find requested element. Key attributes for
                       arbitrary elements are ``id`` and ``name``. See `introduction` for
                       details about locating elements.
        Examples:
        | Scroll Element Into View | css=div.class |
        """
        zoomba.log("Scrolling element '%s' into view." % locator, level='INFO')
        element = self.find_element(locator=locator)
        script = 'arguments[0].scrollIntoView()'
        self.driver.execute_script(script, element)