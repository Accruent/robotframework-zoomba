from AppiumLibrary import AppiumLibrary
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains

zoomba = BuiltIn()


class MobileLibrary(AppiumLibrary):
    """Zoomba Mobile Library

        This class is the base Library used to generate automated Mobile Tests in the Robot Automation Framework using
        Appium. This Library uses and extends the robotframework-appiumlibrary.

    = Locating or Specifying Elements =

    All keywords in MobileLibrary that need to find an element on the page take an argument, either a
    ``locator`` or a ``webelement``. ``locator`` is a string that describes how to locate an element using a syntax
    specifying different location strategies. ``webelement`` is a variable that
    holds a WebElement instance, which is a representation of the element.

    == Using locators ==

    By default, when a locator is provided, it is matched against the key attributes
    of the particular element type. For iOS and Android, key attribute is ``id`` for
    all elements and locating elements is easy using just the ``id``. For example:

    | Click Element    id=my_element

    ``id`` and ``xpath`` are not required to be specified,
    however ``xpath`` should start with ``//`` else just use ``xpath`` locator as explained below.

    For example:

    | Click Element    my_element
    | Wait Until Page Contains Element    //*[@type="android.widget.EditText"]


    Appium additionally supports some of the [https://w3c.github.io/webdriver/webdriver-spec.html|Mobile JSON Wire Protocol] locator strategies.
    It is also possible to specify the approach MobileLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     | *Note*                      |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id attribute          |                             |
    | id                | Click Element `|` id=my_element                                | Matches by @resource-id attribute |                             |
    | accessibility_id  | Click Element `|` accessibility_id=button3                     | Accessibility options utilize.    |                             |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |                             |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |                             |
    | android           | Click Element `|` android=UiSelector().description('Apps')     | Matches by Android UI Automator   |                             |
    | ios               | Click Element `|` ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |                             |
    | nsp               | Click Element `|` nsp=name=="login"                            | Matches by iOSNsPredicate         |                             |
    | css               | Click Element `|` css=.green_button                            | Matches by css in webview         |                             |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        | *Only valid* for Selendroid |

    == Using webelements ==

    One can pass an argument that contains a WebElement instead of a string locator.
    To get a WebElement, use the new `Get WebElements` or `Get WebElement` keyword.

    For example:
    | @{elements}    Get Webelements    class=UIAButton
    | Click Element    @{elements}[2]

    """

    @keyword("Wait For And Clear Text")
    def wait_for_and_clear_text(self, locator, timeout=None, error=None):
        """Wait for and then clear the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.clear_text(locator)

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator, timeout=None, error=None):
        """Wait for and click the element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements.
        
        Use `Wait For And Mouse Over And Click Element` if this keyword gives issues in the application."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.click_element(locator)

    @keyword("Wait For And Click Text")
    def wait_for_and_click_text(self, text, exact_match=False, timeout=None, error=None):
        """Wait for and click text identified by ``text``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        By default tries to click first text involves given ``text``. If you would
        like to click exactly matching text, then set ``exact_match`` to `True`.
        
        Use `Wait For And Mouse Over And Click Text` if this keyword gives issues in the application."""
        self.wait_until_page_contains(text, timeout, error)
        self.click_text(text, exact_match)

    @keyword("Wait For And Input Password")
    def wait_for_and_input_password(self, locator, text, timeout=None, error=None):
        """Wait for and type the given password into the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        The difference between this keyword and `Wait For And Input Text` is that this keyword
        does not log the given password. See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.input_password(locator, text)

    @keyword("Wait For And Input Text")
    def wait_for_and_input_text(self, locator, text, timeout=None, error=None):
        """Wait for and type the given ``locator`` into text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.input_text(locator, text)

    @keyword("Wait For And Long Press")
    def wait_for_and_long_press(self, locator, duration=5000, timeout=None, error=None):
        """Wait for and long press the element identified by ``locator`` with optional duration.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.long_press(locator, duration)

    @keyword("Wait Until Element Contains")
    def wait_until_element_contains(self, locator, text, timeout=None, error=None):
        """Waits until element specified with ``locator`` contains ``text``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_contain_text(locator, text, error)

    @keyword("Wait Until Element Does Not Contain")
    def wait_until_element_does_not_contain(self, locator, text, timeout=None, error=None):
        """Waits until element specified with ``locator`` does not contain ``text``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Contains`,
        `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_not_contain_text(locator, text, error)

    @keyword("Wait Until Element Is Enabled")
    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is enabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_enabled(locator)

    @keyword("Wait Until Element Is Disabled")
    def wait_until_element_is_disabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is disabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_disabled(locator)

    @keyword("Drag And Drop")
    def drag_and_drop(self, source, target):
        """Drags the element found with the locator  ``source`` to the element found with the locator ``target``.
        """
        driver = self._current_application()
        source_element = self._element_find(source, True, True)
        target_element = self._element_find(target, True, True)
        actions = ActionChains(driver)
        actions.drag_and_drop(source_element, target_element).perform()

    @keyword("Drag And Drop By Offset")
    def drag_and_drop_by_offset(self, locator, x_offset=0, y_offset=0):
        """Drags the element found with ``locator`` to the given ``x_offset`` and ``y_offset`` coordinates.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        actions = ActionChains(driver)
        actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()

    # Private
    # @staticmethod
    # def _move_to_element(actions, element, x_offset, y_offset):
    #     if x_offset != 0 or y_offset != 0:
    #         actions.move_to_element_with_offset(element, x_offset, y_offset)
    #     else:
    #         actions.move_to_element(element)
