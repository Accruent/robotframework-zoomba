from AppiumLibrary import AppiumLibrary
from selenium.common.exceptions import WebDriverException
from appium import webdriver
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from contextlib import suppress

zoomba = BuiltIn()


class DesktopLibrary(AppiumLibrary):
    """Zoomba Desktop Library
        This class is the base Library used to generate automated Desktop Tests in the Robot Automation Framework using
        Appium. This Library uses and extends the robotframework-appiumlibrary.

    = Locating or Specifying Elements =

    All keywords in DesktopLibrary that need to find an element on the page take a locator argument. To find these
    locators we use **inspect.exe**. Microsoft Visual Studio 2015 by default includes Windows SDK that provides
    great tool to inspect the application you are testing. This tool allows you to see every UI element/node that you
    can interact with using DesktopLibrary. This **inspect.exe** tool can be found under the Windows SDK folder such as
    `C:\Program Files (x86)\Windows Kits\\10\\bin\\x86`. The tool will show various element attributes. The table below
    shows you witch locator strategy you should use to find elements with the corresponding attributes.

    | *Locator Strategy* | *Matched Attribute in inspect.exe* | *Example*                                         |
    |  accessibility id  |            AutomationId            | Click Element `|` accessibility_id=my_element_id  |
    |       class        |              ClassName             | Click Element `|` class=UIAPickerWheel            |
    |       name         |                Name                | Click Element `|` name=my_element                 |

    Example tests using the windows calculator are located in the tests directory.

    """

    def get_keyword_names(self):
        """
        This function restricts the keywords used in the library. This is to prevent incompatible keywords from imported
        libraries from being referenced and used.
        """
        return [
            'maximize_window', 'open_application', 'wait_for_and_clear_text', 'wait_for_and_click_element',
            'wait_for_and_click_text', 'wait_for_and_input_password', 'wait_for_and_input_text',
            'wait_for_and_long_press', 'wait_until_element_contains', 'wait_until_element_does_not_contain',
            'wait_until_element_is_enabled', 'wait_until_element_is_disabled',
            # External Libraries
            'capture_page_screenshot', 'clear_text', 'click_a_point', 'click_button', 'click_element',
            'click_element_at_coordinates', 'click_text', 'close_all_applications', 'close_application',
            'element_attribute_should_match', 'element_should_be_disabled', "element_should_be_enabled",
            'element_should_be_visible', 'element_should_contain_text', 'element_should_not_contain_text',
            'element_text_should_be', 'get_appium_sessionId', 'get_appium_timeout', 'get_capability',
            'get_element_attribute', 'get_element_location', 'get_element_size', 'get_webelement',
            'get_webelements', 'get_window_height', 'get_window_width', 'input_password', 'input_text',
            'launch_application', 'log_source', 'long_press', 'page_should_contain_element', 'page_should_contain_text',
            'page_should_not_contain_element', 'page_should_not_contain_text', 'quit_application',
            'register_keyword_to_run_on_failure', 'set_appium_timeout', 'switch_application', 'text_should_be_visible',
            'wait_until_element_is_visible', 'wait_until_page_contains', 'wait_until_page_contains_element',
            'wait_until_page_does_not_contain', 'wait_until_page_does_not_contain_element', 'get_matching_xpath_count',
            'xpath_should_match_x_times'
        ]

    @keyword("Maximize Window")
    def maximize_window(self):
        """Maximizes the current application window.

        Windows Only.
        """
        driver = self._current_application()
        driver.maximize_window()
        return True

    @keyword("Open Application")
    def open_application(self, remote_url, alias=None, window_name=None, **kwargs):
        """Opens a new application to given Appium server.
        Capabilities of appium server, Windows,
        Please check http://appium.io/docs/en/drivers/windows
        | *Option*            | *Man.* | *Description*     |
        | remote_url          | Yes    | Appium server url |
        | alias               | no     | alias             |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          |
        """
        desired_caps = kwargs
        if window_name:
            """ 
            If the app has a splash screen we need to supply the window_name of the final window. This code path will 
            start the application and then attach to the correct window via the window_name.
            """
            with suppress(WebDriverException):
                # Ignore WebDriverException if the app has a splash screen
                webdriver.Remote(str(remote_url), desired_caps)
            desktop_capabilities = dict()
            desktop_capabilities.update({"app": "Root", "platformName": "Windows", "deviceName": "WindowsPC"})
            desktop_session = webdriver.Remote(str(remote_url), desktop_capabilities)
            window = desktop_session.find_element_by_name(window_name)
            window = hex(int(window.get_attribute("NativeWindowHandle")))
            if "app" in desired_caps:
                del desired_caps["app"]
            desired_caps["appTopLevelWindow"] = window
        # global application
        application = webdriver.Remote(str(remote_url), desired_caps)
        self._debug('Opened application with session id %s' % application.session_id)

        return self._cache.register(application, alias)

    @keyword("Wait For And Clear Text")
    def wait_for_and_clear_text(self, locator, timeout=None, error=None):
        """Wait for and then clear the text field identified by `locator`.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.clear_text(locator)

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator, timeout=None, error=None):
        """Wait for and click the element identified by `locator`.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.click_element(locator)

    @keyword("Wait For And Click Text")
    def wait_for_and_click_text(self, text, exact_match=False, timeout=None, error=None):
        """Wait for and click text identified by ``text``.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        By default tries to click first text involves given ``text``, if you would
        like to click exactly matching text, then set ``exact_match`` to `True`."""
        self.wait_until_page_contains(text, timeout, error)
        self.click_text(text, exact_match)

    @keyword("Wait For And Input Password")
    def wait_for_and_input_password(self, locator, text, timeout=None, error=None):
        """Wait for and type the given password into the text field identified by `locator`.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        The difference between this keyword and `Wait For And Input Text` is that this keyword
        does not log the given password. See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.input_password(locator, text)

    @keyword("Wait For And Input Text")
    def wait_for_and_input_text(self, locator, text, timeout=None, error=None):
        """Wait for and type the given `text` into text field identified by `locator`.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.input_text(locator, text)

    @keyword("Wait For And Long Press")
    def wait_for_and_long_press(self, locator, duration=10000, timeout=None, error=None):
        """Wait for and long press the element identified by `locator` with optional duration.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.long_press(locator, duration)

    @keyword("Wait Until Element Contains")
    def wait_until_element_contains(self, locator, text, timeout=None, error=None):
        """Waits until element specified with `locator` contains 'text'.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_contain_text(locator, text, error)

    @keyword("Wait Until Element Does Not Contain")
    def wait_until_element_does_not_contain(self, locator, text, timeout=None, error=None):
        """Waits until element specified with `locator` does not contain 'text'.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See also 'Wait Until Element Contains,
        `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_not_contain_text(locator, text, error)

    @keyword("Wait Until Element Is Enabled")
    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` is enabled.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See also 'Wait Until Element Is Disabled'
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_enabled(locator)

    @keyword("Wait Until Element Is Disabled")
    def wait_until_element_is_disabled(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` is disabled.

        Fails if `timeout` expires before the element appears.

        `error` can be used to override the default error message.

        See also 'Wait Until Element Is Disabled'
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.element_should_be_disabled(locator)

    # @keyword("Mouse Over Element")
    # def mouse_over_element(self, locator, timeout=None, error=None):
    #     """Waits until element specified with `locator` is disabled.
    #
    #     Fails if `timeout` expires before the element appears.
    #
    #     `error` can be used to override the default error message.
    #
    #     See also 'Wait Until Element Is Disabled'
    #     """
    #     location = webdriver.Remote.find_element_by_accessibility_id(locator)
    #     webdriver.Remote.Mouse

