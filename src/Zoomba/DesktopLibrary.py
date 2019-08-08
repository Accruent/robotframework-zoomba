from AppiumLibrary import AppiumLibrary
from appium import webdriver
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import os
from selenium.webdriver.common.action_chains import ActionChains

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

    = Use of Wait Keywords =

    When using a modern Windows application there should be no issue with using the 'Wait For And' keywords. However if
    you are using an older WinForm, Win32, or a larger application it may be necessary to simply use the non-waiting
    version of keywords. Then you would simply add your waits in manually where necessary using something like
    `Wait Until Page Contains` or `Wait Until Page Contains Element`.

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
            'wait_until_element_is_enabled', 'wait_until_element_is_disabled', 'switch_application_by_name',
            'mouse_over_element', 'wait_for_and_mouse_over_element', 'mouse_over_and_click_element',
            'wait_for_and_mouse_over_and_click_element','mouse_over_text', 'wait_for_and_mouse_over_text',
            'mouse_over_and_click_text', 'wait_for_and_mouse_over_and_click_text',
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
        If your application has a splash screen please supply the window name of the final window that will appear.
        For the capabilities of appium server and Windows,
        Please check http://appium.io/docs/en/drivers/windows
        | *Option*            | *Man.* | *Description*                                                        |
        | remote_url          | Yes    | Appium server url                                                    |
        | alias               | No     | Alias                                                                |
        | window_name         | No     | Window name you wish to attach, usually after a splash screen        |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          |
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          | window_name=MyApplication          |
        """
        desired_caps = kwargs
        if window_name:
            # """
            # If the app has a splash screen we need to supply the window_name of the final window. This code path will
            # start the application and then attach to the correct window via the window_name.
            # """
            os.startfile(desired_caps['app'])
            return self.switch_application_by_name(remote_url, alias=alias, window_name=window_name, **kwargs)
        else:
            # global application
            application = webdriver.Remote(str(remote_url), desired_caps)
            self._debug('Opened application with session id %s' % application.session_id)

            return self._cache.register(application, alias)

    @keyword("Switch Application By Name")
    def switch_application_by_name(self, remote_url, window_name, alias=None, **kwargs):
        """Switches to a currently opened window by name.
        For the capabilities of appium server and Windows,
        Please check http://appium.io/docs/en/drivers/windows
        | *Option*            | *Man.* | *Description*                         |
        | remote_url          | Yes    | Appium server url                     |
        | window_name         | Yes    | Window name you wish to attach        |
        | alias               | No     | alias                                 |

        Examples:
        | Switch Application By Name | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | window_name=MyApplication         |
        """
        desired_caps = kwargs
        desktop_capabilities = dict()
        desktop_capabilities.update({"app": "Root", "platformName": "Windows", "deviceName": "WindowsPC"})
        desktop_session = webdriver.Remote(str(remote_url), desktop_capabilities)
        window = desktop_session.find_element_by_name(window_name)
        window = hex(int(window.get_attribute("NativeWindowHandle")))
        desktop_session.quit()
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

    @keyword("Mouse Over Element")
    def mouse_over_element(self, locator):
        """Moves the mouse over the given locator.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()

    @keyword("Wait For And Mouse Over Element")
    def wait_for_and_mouse_over_element(self, locator, timeout=None, error=None):
        """Waits for and moves the mouse over the given locator.
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.mouse_over_element(locator)

    @keyword("Mouse Over And Click Element")
    def mouse_over_and_click_element(self, locator, double_click=False):
        """Moves the mouse over and clicks the given locator.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        if double_click:
            actions.double_click()
        else:
            actions.click()
        actions.perform()

    @keyword("Wait For And Mouse Over And Click Element")
    def wait_for_and_mouse_over_and_click_element(self, locator, timeout=None, error=None, double_click=False):
        """Waits for, moves the mouse over, and clicks the given locator.
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.mouse_over_and_click_element(locator, double_click)

    @keyword("Mouse Over Text")
    def mouse_over_text(self, text, exact_match=False):
        """Moves the mouse over the given text.
        """
        self.mouse_over_element('name=' + text)
        # driver = self._current_application()
        # element = self._element_find_by_text(text, exact_match)
        # actions = ActionChains(driver)
        # print('before element move')
        # actions.move_to_element(element)
        # print('after element move')
        # actions.perform()

    @keyword("Wait For And Mouse Over Text")
    def wait_for_and_mouse_over_text(self, text, exact_match=False, timeout=None, error=None):
        """Moves the mouse over the given text.
        """
        self.wait_until_page_contains(text, timeout, error)
        self.mouse_over_text(text, exact_match)

    @keyword("Mouse Over And Click Text")
    def mouse_over_and_click_text(self, text, exact_match=False, double_click=False):
        """Moves the mouse over  and clicks the given text.
        """
        driver = self._current_application()
        element = self._element_find_by_text(text, exact_match)
        actions = ActionChains(driver)
        actions.move_to_element(element)
        if double_click:
            actions.double_click()
        else:
            actions.click()
        actions.perform()

    @keyword("Wait For And Mouse Over And Click Text")
    def wait_for_and_mouse_over_and_click_text(self, text, exact_match=False, timeout=None, error=None,
                                               double_click=False):
        """Moves the mouse over the given text.
        """
        self.wait_until_page_contains(text, timeout, error)
        self.mouse_over_and_click_text(text, exact_match, double_click)

    # def _element_find_by_text(self, text, exact_match=False):
    #     # if self._get_platform() == 'ios':
    #     #     element = self._element_find(text, True, False)
    #     #     if element:
    #     #         return element
    #     #     else:
    #     #         if exact_match:
    #     #             _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
    #     #         else:
    #     #             _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
    #     #         return self._element_find(_xpath, True, True)
    #
    #     if exact_match:
    #         _xpath = u'//*[@{}="{}"]'.format('Name', text)
    #     else:
    #         _xpath = u'//*[contains(@{},"{}")]'.format('Name', text)
    #     return self._element_find(_xpath, True, True)