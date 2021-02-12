import importlib
from AppiumLibrary import AppiumLibrary
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

try:
    AppiumCommon = importlib.import_module('Helpers.AppiumCommon', package='Helpers')
except ModuleNotFoundError:
    AppiumCommon = importlib.import_module('.Helpers.AppiumCommon', package='Zoomba')

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

    def __init__(self, timeout=5, run_on_failure='Save Appium Screenshot'):
        """MobileLibrary can be imported with optional arguments.
        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.
        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a MobileLibrary keyword fails.
        By default `Save Appium Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.
        Examples:
        | Library | MobileLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | MobileLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        super().__init__(timeout, run_on_failure)

    @keyword("Wait For And Clear Text")
    def wait_for_and_clear_text(self, locator, timeout=None, error=None):
        """Wait for and then clear the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.clear_text(locator)

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator, timeout=None, error=None):
        """Wait for and click the element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.click_element(locator)

    @keyword("Wait For And Click Text")
    def wait_for_and_click_text(self, text, exact_match=False, timeout=None, error=None):
        """Wait for and click text identified by ``text``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        By default tries to click first text involves given ``text``. If you would
        like to click exactly matching text, then set ``exact_match`` to `True`."""
        self._wait_until_page_contains(text, timeout, error)
        self.click_text(text, exact_match)

    @keyword("Wait For And Click Button")
    def wait_for_and_click_button(self, locator, timeout=None, error=None):
        """Wait for and click the button identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.click_button(locator)

    @keyword("Wait For And Input Password")
    def wait_for_and_input_password(self, locator, text, timeout=None, error=None):
        """Wait for and type the given password into the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        The difference between this keyword and `Wait For And Input Text` is that this keyword
        does not log the given password. See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.input_password(locator, text)

    @keyword("Wait For And Input Text")
    def wait_for_and_input_text(self, locator, text, timeout=None, error=None):
        """Wait for and type the given ``locator`` into text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.input_text(locator, text)

    @keyword("Wait For And Input Value")
    def wait_for_and_input_value(self, locator, value, timeout=None, error=None):
        """Wait for and set the given ``value`` into the text field identified by ``locator``.
        This is an IOS only keyword, input value makes use of set_value.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        The difference between this keyword and `Wait For And Input Text` is that this keyword
        does not log the given password. See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.input_value(locator, value)

    @keyword("Wait For And Long Press")
    def wait_for_and_long_press(self, locator, duration=5000, timeout=None, error=None):
        """Wait for and long press the element identified by ``locator`` with optional duration.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
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
        self._wait_until_page_contains_element(locator, timeout, error)
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
        self._wait_until_page_contains_element(locator, timeout, error)
        self.element_should_not_contain_text(locator, text, error)

    @keyword("Wait Until Element Is Enabled")
    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is enabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        self._wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_enabled(locator)

    @keyword("Wait Until Element Is Disabled")
    def wait_until_element_is_disabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is disabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        self._wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_disabled(locator)

    @keyword("Drag And Drop")
    def drag_and_drop(self, source, target):
        """Drags the element found with the locator ``source`` to the element found with the
        locator ``target``."""
        AppiumCommon.drag_and_drop(self, source, target)

    @keyword("Drag And Drop By Offset")
    def drag_and_drop_by_offset(self, locator, x_offset=0, y_offset=0):
        """Drags the element found with ``locator`` to the given ``x_offset`` and ``y_offset``
        coordinates.
        """
        AppiumCommon.drag_and_drop_by_offset(self, locator, x_offset, y_offset)

    @keyword("Scroll Down To Text")
    def scroll_down_to_text(self, text, swipe_count=20):
        """Scrolls down to ``text`` using small swipes. The ``swipe_count`` defaults to 20."""
        found = False
        for x in range(swipe_count):
            if self._is_text_present(text):
                found = True
                break
            else:
                self.swipe_by_percent(50, 75, 50, 50)  # use swipe by direction if its ever implemented
        if not found:
            zoomba.fail("Text: " + text + " was not found after " + str(swipe_count) + " swipes")

    @keyword("Scroll Up To Text")
    def scroll_up_to_text(self, text, swipe_count=20):
        """Scrolls down to ``text`` using small swipes. The ``swipe_count`` defaults to 20."""
        found = False
        for x in range(swipe_count):
            if self._is_text_present(text):
                found = True
                break
            else:
                self.swipe_by_percent(50, 50, 50, 75)  # use swipe by direction if its ever implemented
        if not found:
            zoomba.fail("Text: " + text + " was not found after " + str(swipe_count) + " swipes")

    @keyword("Wait For And Tap")
    def wait_for_and_tap(self, locator, x_offset=None, y_offset=None, count=1, timeout=None,
                         error=None):
        """ Wait for and then Tap element identified by ``locator``.
        Args:
        - ``x_offset`` - (optional) x coordinate to tap, relative to the top left corner of the element.
        - ``y_offset`` - (optional) y coordinate. If y is used, x must also be set, and vice versa
        - ``count`` - can be used to tap multiple times
        - ``timeout`` - time in seconds to locate the element, defaults to global timeout
        - ``error`` - (optional) used to override the default error message.
        """
        self._wait_until_page_contains_element(locator, timeout, error)
        self.tap(locator, x_offset, y_offset, count)

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `appium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.

        See `Save Appium Screenshot` for a screenshot that will be unique across reports
        """
        return AppiumCommon.capture_page_screenshot(self, filename)

    @keyword("Save Appium Screenshot")
    def save_appium_screenshot(self):
        """Takes a screenshot with a unique filename to be stored in Robot Framework compiled
        reports."""
        return AppiumCommon.save_appium_screenshot(self)
    
    # Private
    def _wait_until_page_contains(self, text, timeout=None, error=None):
        """Internal version to avoid duplicate screenshots"""
        AppiumCommon.wait_until_page_contains(self, text, timeout, error)

    def _wait_until_page_contains_element(self, locator, timeout=None, error=None):
        """Internal version to avoid duplicate screenshots"""
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)
