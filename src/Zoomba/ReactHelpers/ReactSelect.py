# Similar to the Select class found in the Selenium Library:
#   https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/support/select.py
# Uses <div> tags instead of <select> & <option>
# See the ReactHelpers/README.md for more information on the structure of React-Select components

from selenium.common.exceptions import UnexpectedTagNameException


class ReactSelect:

    def __init__(self, webelement):
        """
        Constructor. A check is made that the given element is, indeed, a DIV tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - webelement - The React-Select container <div> element.

        Example:
            from ReactSelect import ReactSelect as RS
            react_select_container = self.find_element(locator)
            options = RS.ReactSelect(react_select_container).options()
        """
        if webelement.tag_name.lower() != "div":
            raise UnexpectedTagNameException(
                "ReactSelect only works on <div> elements, not on <%s>" %
                webelement.tag_name)
        self._el = webelement

    def options(self):
        """Returns a list of all options belonging to the React-Select container"""
        self.expand_select_list()
        return self._el.find_elements_by_xpath('./div[2]/div[1]/div')

    def is_expanded(self):
        """Checks if the React-Select container is expanded by checking if the Menu <div> exists as a child of the container"""
        menu_elements = self._el.find_elements_by_xpath('./div[2]')
        if len(menu_elements) == 0:
            return False
        if len(menu_elements) == 1:
            return True
        raise LookupError("ReactSelect.is_expanded: Multiple selection menus found")

    def expand_select_list(self):
        is_expanded = self.is_expanded()
        if not is_expanded:
            self._el.click()
