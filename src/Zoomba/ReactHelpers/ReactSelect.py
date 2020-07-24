from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException


class ReactSelect(Select):  # ToDo: Update documentation
    # Examples: https://react-select.com/home
    # Note: "Options" typically don't appear in the page's source html until the drop-down is clicked/expanded, so the locator for those can be tricky

    def __init__(self, webelement):
        """
        Constructor. A check is made that the given element is, indeed, a SELECT tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - webelement - element SELECT element to wrap

        Example:
            from selenium.webdriver.support.ui import Select \n
            Select(driver.find_element_by_tag_name("select")).select_by_index(2)
        """
        if webelement.tag_name.lower() != "div":
            raise UnexpectedTagNameException(
                "ReactSelect only works on <div> elements, not on <%s>" %
                webelement.tag_name)
        self._el = webelement
        multi = self._el.get_attribute("multiple")
        self.is_multiple = multi and multi != "false"

    @property
    def options(self):
        """Returns a list of all options belonging to this div tag"""
        return self._el.find_elements(By.TAG_NAME, 'div')

    def select_by_visible_text(self, text):
        """Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specified text in SELECT
           """
        xpath = ".//div[normalize-space(.) = %s]" % self._escapeString(text)
        opts = self._el.find_elements(By.XPATH, xpath)
        matched = False
        for opt in opts:
            self._setSelected(opt)
            if not self.is_multiple:
                return
            matched = True

        if len(opts) == 0 and " " in text:
            subStringWithoutSpace = self._get_longest_token(text)
            if subStringWithoutSpace == "":
                candidates = self.options
            else:
                xpath = ".//div[contains(.,%s)]" % self._escapeString(subStringWithoutSpace)
                candidates = self._el.find_elements(By.XPATH, xpath)
            for candidate in candidates:
                if text == candidate.text:
                    self._setSelected(candidate)
                    if not self.is_multiple:
                        return
                    matched = True

        if not matched:
            raise NoSuchElementException("Could not locate element with visible text: %s" % text)

