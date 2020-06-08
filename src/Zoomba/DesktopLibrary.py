import itertools
from AppiumLibrary import AppiumLibrary
from appium import webdriver
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess

from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time

zoomba = BuiltIn()
SCREENSHOT_COUNTER = itertools.count()


class DesktopLibrary(AppiumLibrary):
    """Zoomba Desktop Library

    This class is the base Library used to generate automated Desktop Tests in the Robot Automation Framework using
    Appium. This Library uses and extends the robotframework-appiumlibrary.

    = Locating or Specifying Elements =

    All keywords in DesktopLibrary that need to find an element on the page take a locator argument. To find these
    locators we use **Accessibility Insights** to inspect the application under test. This tool allows you to see every
    UI element/node that you can interact with using DesktopLibrary. **Accessibility Insights** can be downloaded at
    https://accessibilityinsights.io/ The tool will show various element attributes. The table below
    shows you witch locator strategy you should use to find elements with the corresponding attributes.

    To locate xpath we suggest using the **WinAppDriver UI Recorder** located here:
    https://github.com/Microsoft/WinAppDriver/releases

    | *Locator Strategy* | *Matched Attribute in Insights*    | *Example*                                         |
    |  accessibility_id  |            AutomationId            | Click Element `|` accessibility_id=my_element_id  |
    |       class        |              ClassName             | Click Element `|` class=UIAPickerWheel            |
    |       name         |                Name                | Click Element `|` name=my_element                 |
    |       xpath        |                N/A                 | Click Element `|` xpath=//Button[@Name="Close"]   |

    Example tests using the windows calculator are located in the tests directory.

    = Use of Wait Keywords =

    When using a modern Windows application there should be no issue with using the 'Wait For And' keywords. However if
    you are using an older WinForm, Win32, or a larger application it may be necessary to simply use the non-waiting
    version of keywords. Then you would simply add your waits in manually where necessary using something like
    ``Wait Until Page Contains`` or ``Wait Until Page Contains Element``.
    """

    def __init__(self, timeout=5, run_on_failure='Save Appium Screenshot'):
        """DesktopLibrary can be imported with optional arguments.
        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.
        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a DesktopLibrary keyword fails.
        By default `Save Appium Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.
        Examples:
        | Library | DesktopLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | DesktopLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        super().__init__(timeout, run_on_failure)

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
            'wait_for_and_mouse_over_and_click_element', 'mouse_over_text', 'wait_for_and_mouse_over_text',
            'mouse_over_and_click_text', 'wait_for_and_mouse_over_and_click_text', 'click_a_point',
            'context_click_a_point', 'mouse_over_and_context_click_element', 'mouse_over_and_context_click_text',
            'mouse_over_by_offset', 'drag_and_drop', 'drag_and_drop_by_offset', 'send_keys', 'send_keys_to_element',
            'capture_page_screenshot', 'save_appium_screenshot', 'select_element_from_combobox', 'get_source',
            'click_text',
            # External Libraries
            'clear_text', 'click_button', 'click_element', 'close_all_applications', 'close_application',
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
        """
        driver = self._current_application()
        driver.maximize_window()
        return True

    @keyword("Open Application")
    def open_application(self, remote_url, alias=None, window_name=None, splash_delay=0, **kwargs):
        """Opens a new application to given Appium server.
        If your application has a splash screen please supply the window name of the final window that will appear.
        For the capabilities of appium server and Windows please check http://appium.io/docs/en/drivers/windows

        | *Option*            | *Man.* | *Description*                                                        |
        | remote_url          | Yes    | Appium server url                                                    |
        | alias               | No     | Alias                                                                |
        | window_name         | No     | Window name you wish to attach, usually after a splash screen        |
        | splash_delay        | No     | Delay used when waiting for a splash screen to load, in seconds      |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          |
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          | window_name=MyApplication          | splash_delay=5          |

        A session for the root desktop will also be opened and can be switched to by running the following:
        | Switch Application | Desktop         |
        """
        desired_caps = kwargs

        if window_name:
            # If the app has a splash screen we need to supply the window_name of the final window. This code path will
            # start the application and then attach to the correct window via the window_name.
            self._info('Opening application "%s"' % desired_caps['app'])
            subprocess.Popen(desired_caps['app'])
            if splash_delay > 0:
                self._info('Waiting %s seconds for splash screen' % splash_delay)
                sleep(splash_delay)
            return self.switch_application_by_name(remote_url, alias=alias, window_name=window_name, **kwargs)
        # global application
        self._open_desktop_session(remote_url)
        application = webdriver.Remote(str(remote_url), desired_caps)
        self._debug('Opened application with session id %s' % application.session_id)
        return self._cache.register(application, alias)

    @keyword("Switch Application By Name")
    def switch_application_by_name(self, remote_url, window_name, alias=None, **kwargs):
        """Switches to a currently opened window by ``window_name``.
        For the capabilities of appium server and Windows,
        Please check http://appium.io/docs/en/drivers/windows
        | *Option*            | *Man.* | *Description*                         |
        | remote_url          | Yes    | Appium server url                     |
        | window_name         | Yes    | Window name you wish to attach        |
        | alias               | No     | alias                                 |

        Examples:
        | Switch Application By Name | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | window_name=MyApplication         |

        A session for the root desktop will also be opened and can be switched to by running the following:
        | Switch Application | Desktop         |
        """
        desired_caps = kwargs
        desktop_session = self._open_desktop_session(remote_url)
        try:
            window = desktop_session.find_element_by_name(window_name)
            self._debug('Window_name "%s" found.' % window_name)
            window = hex(int(window.get_attribute("NativeWindowHandle")))
        except Exception as e:
            self._debug('Closing desktop session.')
            zoomba.fail(
                'Error finding window "' + window_name + '" in the desktop session. '
                                                         'Is it a top level window handle?' + '. \n' + str(e))
        if "app" in desired_caps:
            del desired_caps["app"]
        desired_caps["appTopLevelWindow"] = window
        # global application
        try:
            self._info('Connecting to window_name "%s".' % window_name)
            application = webdriver.Remote(str(remote_url), desired_caps)
        except Exception as e:
            zoomba.fail(
                'Error connecting webdriver to window "' + window_name + '". \n' + str(e))
        self._debug('Opened application with session id %s' % application.session_id)
        return self._cache.register(application, alias)

    def launch_application(self):
        """ Launch application. Application can be launched while Appium session running.
        This keyword can be used to launch application during test case or between test cases.

        This keyword works while `Open Application` has a test running. This is good practice to `Launch Application`
        and `Quit Application` between test cases. As Suite Setup is `Open Application`, `Test Setup` can be used to `Launch Application`

        Example (syntax is just a representation, refer to RF Guide for usage of Setup/Teardown):
        | [Setup Suite] |
        |  | Open Application | http://localhost:4723 | platformName=Windows | deviceName=Windows | app=${App_Path} |
        | [Test Setup] |
        |  | Launch Application |
        |  |  | <<<test execution>>> |
        |  |  | <<<test execution>>> |
        | [Test Teardown] |
        |  | Quit Application |
        | [Suite Teardown] |
        |  | Close Application |

        See `Quit Application` for quiting application but keeping Appium session running.
        """
        self._open_desktop_session(self._current_application().command_executor)
        driver = self._current_application()
        driver.launch_app()

    @keyword("Wait For And Clear Text")
    def wait_for_and_clear_text(self, locator, timeout=None, error=None):
        """Wait for and then clear the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.clear_text(locator)

    def click_element(self, locator):
        """Click element identified by `locator`.

        Supported prefixes: ``accessibility_id``, ``name``, ``class``, ``xpath``

        If no prefix is given ``click element`` defaults to ``accessibility_id`` or ``xpath``
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator, timeout=None, error=None):
        """Wait for and click the element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements.
        
        Use `Wait For And Mouse Over And Click Element` if this keyword gives issues in the application."""
        self.wait_until_page_contains_element(locator, timeout, error)
        self.click_element(locator)

    @keyword("Click Text")
    def click_text(self, text, exact_match=False):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Click Element` with the ``name`` prefix instead.
        """
        self._element_find_by_text(text, exact_match).click()

    @keyword("Wait For And Click Text")
    def wait_for_and_click_text(self, text, exact_match=False, timeout=None, error=None):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Wait For And Click Element` with the ``name`` prefix instead.
        """
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
    def wait_for_and_long_press(self, locator, duration=10000, timeout=None, error=None):
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

    @keyword("Mouse Over Element")
    def mouse_over_element(self, locator, x_offset=0, y_offset=0):
        """Moves the mouse over the given ``locator``.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        actions = ActionChains(driver)
        self._move_to_element(actions, element, x_offset, y_offset)
        actions.perform()

    @keyword("Wait For And Mouse Over Element")
    def wait_for_and_mouse_over_element(self, locator, timeout=None, error=None, x_offset=0, y_offset=0):
        """Waits for and moves the mouse over the given ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.mouse_over_element(locator, x_offset, y_offset)

    @keyword("Mouse Over And Click Element")
    def mouse_over_and_click_element(self, locator, double_click=False, x_offset=0, y_offset=0):
        """Moves the mouse over and clicks the given ``locator``.

        ``double_click`` can be used to click twice.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        self.mouse_over_element(locator, x_offset=x_offset, y_offset=y_offset)
        self.click_a_point(double_click=double_click)

    @keyword("Mouse Over And Context Click Element")
    def mouse_over_and_context_click_element(self, locator, x_offset=0, y_offset=0):
        """Moves the mouse over and right-clicks the given ``locator``.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.

        See also `Mouse Over And Click Element`
        """
        self.mouse_over_element(locator, x_offset=x_offset, y_offset=y_offset)
        self.context_click_a_point()

    @keyword("Wait For And Mouse Over And Click Element")
    def wait_for_and_mouse_over_and_click_element(self, locator, timeout=None, error=None, double_click=False,
                                                  x_offset=0, y_offset=0):
        """Waits for, moves the mouse over, and clicks the given ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        ``double_click`` can be used to click twice.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        self.wait_until_page_contains_element(locator, timeout, error)
        self.mouse_over_and_click_element(locator, double_click, x_offset, y_offset)

    @keyword("Mouse Over Text")
    def mouse_over_text(self, text, exact_match=False, x_offset=0, y_offset=0):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Mouse Over Element` with the ``name`` prefix instead.
        """
        driver = self._current_application()
        element = self._element_find_by_text(text, exact_match)
        actions = ActionChains(driver)
        self._move_to_element(actions, element, x_offset, y_offset)
        actions.perform()

    @keyword("Wait For And Mouse Over Text")
    def wait_for_and_mouse_over_text(self, text, exact_match=False, timeout=None, error=None, x_offset=0, y_offset=0):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Wait For And Mouse Over Element` with the ``name`` prefix instead.
        """
        self.wait_until_page_contains(text, timeout, error)
        self.mouse_over_text(text, exact_match, x_offset, y_offset)

    @keyword("Mouse Over And Click Text")
    def mouse_over_and_click_text(self, text, exact_match=False, double_click=False, x_offset=0, y_offset=0):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Mouse Over And Click Element` with the ``name`` prefix instead.
        """
        self.mouse_over_text(text, exact_match=exact_match, x_offset=x_offset, y_offset=y_offset)
        self.click_a_point(double_click=double_click)

    @keyword("Mouse Over And Context Click Text")
    def mouse_over_and_context_click_text(self, text, exact_match=False, x_offset=0, y_offset=0):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Mouse Over And Context Click Element` with the ``name``
        prefix instead.
        """
        self.mouse_over_text(text, exact_match=exact_match, x_offset=x_offset, y_offset=y_offset)
        self.context_click_a_point()

    @keyword("Wait For And Mouse Over And Click Text")
    def wait_for_and_mouse_over_and_click_text(self, text, exact_match=False, timeout=None, error=None,
                                               double_click=False, x_offset=0, y_offset=0):
        """*DEPRECATED in DesktopLibrary 2.4.0* Use `Wait For And Mouse Over And Click Element` with the ``name``
         prefix instead.
        """
        self.wait_until_page_contains(text, timeout, error)
        self.mouse_over_and_click_text(text, exact_match, double_click, x_offset, y_offset)

    @keyword("Mouse Over By Offset")
    def mouse_over_by_offset(self, x_offset=0, y_offset=0):
        """Moves the mouse from its current location by the given ``x_offset`` and ``y_offset``.
        """
        driver = self._current_application()
        actions = ActionChains(driver)
        actions.move_by_offset(x_offset, y_offset)
        self._info('Moving mouse from current location with an offset of (%s,%s).' % (x_offset, y_offset))
        actions.perform()

    @keyword("Click A Point")
    def click_a_point(self, x_offset=0, y_offset=0, double_click=False):
        """Clicks the current mouse location.

        ``x_offset`` and ``y_offset`` can be applied to give an offset.

        ``double_click`` can be used to click twice.
        """
        driver = self._current_application()
        actions = ActionChains(driver)
        if x_offset != 0 or y_offset != 0:
            actions.move_by_offset(x_offset, y_offset)
        if double_click:
            actions.double_click()
        else:
            actions.click()
        self._info("Clicking on current mouse position with an offset of (%s,%s)." % (x_offset, y_offset))
        actions.perform()

    @keyword("Context Click A Point")
    def context_click_a_point(self, x_offset=0, y_offset=0):
        """Right-clicks the current mouse location.

        ``x_offset`` and ``y_offset`` can be applied to give an offset.
        """
        driver = self._current_application()
        actions = ActionChains(driver)
        if x_offset != 0 or y_offset != 0:
            actions.move_by_offset(x_offset, y_offset)
        actions.context_click()
        self._info("Right-clicking on current mouse position with an offset of (%s,%s)." % (x_offset, y_offset))
        actions.perform()

    @keyword("Drag And Drop")
    def drag_and_drop(self, source, target):
        """Drags the element found with the locator ``source`` to the element found with the locator ``target``.
        """
        driver = self._current_application()
        source_element = self._element_find(source, True, True)
        target_element = self._element_find(target, True, True)
        actions = ActionChains(driver)
        self._info('Dragging source element "%s" to target element "%s".' % (source, target))
        actions.drag_and_drop(source_element, target_element).perform()

    @keyword("Drag And Drop By Offset")
    def drag_and_drop_by_offset(self, locator, x_offset=0, y_offset=0):
        """Drags the element found with ``locator`` to the given ``x_offset`` and ``y_offset`` coordinates.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        actions = ActionChains(driver)
        self._info('Dragging element "%s" by offset (%s, %s).' % (locator, x_offset, y_offset))
        actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()

    @keyword("Send Keys")
    def send_keys(self, *argv):
        """Sends the desired keys in ``argv``.

        A list of special key codes can be found
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html|here]

        Note that when sending in a modifier key (Ctrl, Alt, Shift) you will need to send the key again to release it.
        |  Send Keys  |      a              |    b   |
        |  Send Keys  |      \\ue00        |    p    |    \\ue00     |
        """
        driver = self._current_application()
        actions = ActionChains(driver)
        self._info('Sending keys to application')
        if argv:
            for each in argv:
                actions.send_keys(each).perform()
                actions.reset_actions()
        else:
            zoomba.fail('No key arguments specified.')

    @keyword("Send Keys To Element")
    def send_keys_to_element(self, locator, *argv):
        """Sends the desired keys in ``argv`` to ``locator``.

        A list of special key codes can be found
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html|here]

        Note that when sending in a modifier key (Ctrl, Alt, Shift) you will need to send the key again to release it.
        |  Send Keys To Element  |     locator    |      a              |    b   |
        |  Send Keys To Element  |     locator    |      \\ue00        |    p    |    \\ue00     |
        """
        driver = self._current_application()
        actions = ActionChains(driver)
        element = self._element_find(locator, True, True)
        self._info('Sending keys to element "%s".' % locator)
        if argv:
            for each in argv:
                actions.send_keys_to_element(element, each).perform()
                actions.reset_actions()
        else:
            zoomba.fail('No key arguments specified.')

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
        path, link = self._get_screenshot_paths(filename)

        if hasattr(self._current_application(), 'get_screenshot_as_file'):
            self._current_application().get_screenshot_as_file(path)
        else:
            self._current_application().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))
        return link

    @keyword("Save Appium Screenshot")
    def save_appium_screenshot(self):
        """Takes a screenshot with a unique filename to be stored in Robot Framework compiled reports."""
        timestamp = time()
        filename = 'appium-screenshot-' + str(timestamp) + '-' + str(next(SCREENSHOT_COUNTER)) + '.png'
        return self.capture_page_screenshot(filename)

    @keyword("Select Element From ComboBox")
    def select_element_from_combobox(self, list_locator, element_locator, skip_to_desktop=False):
        """Selects the ``element_locator`` from the combobox found by ``list_locator``.

        The keyword first checks the current application for the combobox list elements. If it is not found it will
        switch to the desktop session to look for the elements as many windows applications house the actual combobox
        items in a pane off of the desktop. ``skip_to_desktop`` can be set to ``True`` in order to go straight to the
        desktop session. This provides good time savings when dealing with a large application."""
        self.click_element(list_locator)
        try:
            if skip_to_desktop:
                raise ValueError("Skipping to desktop session")
            self._element_find(element_locator, True, True)
            self.click_element(element_locator)
        except ValueError:
            original_index = self._cache.current_index
            self.switch_application('Desktop')
            self.click_element(element_locator)
            self.switch_application(original_index)

    # Private
    def _element_find_by_text(self, text, exact_match=False):
        if exact_match:
            _xpath = u'//*[@{}="{}"]'.format('Name', text)
        else:
            _xpath = u'//*[contains(@{},"{}")]'.format('Name', text)
        return self._element_find(_xpath, True, True)

    def _move_to_element(self, actions, element, x_offset=0, y_offset=0):
        if x_offset != 0 or y_offset != 0:
            self._info('Moving to element "' + str(element) + '" with offset (%s,%s).' % (x_offset, y_offset))
            actions.move_to_element_with_offset(element, x_offset, y_offset)
        else:
            self._info('Moving to element "' + str(element) + '".')
            actions.move_to_element(element)

    def _open_desktop_session(self, remote_url, alias="Desktop"):
        try:
            return self._cache.get_connection(alias)
        except RuntimeError:
            self._debug('Creating new desktop session')
            desktop_capabilities = dict({"app": "Root", "platformName": "Windows", "deviceName": "Windows",
                                         "newCommandTimeout": 3600})
            desktop_session = webdriver.Remote(str(remote_url), desktop_capabilities)
            self._cache.register(desktop_session, alias=alias)
            return desktop_session

    def _element_find(self, locator, first_only, *kwargs):
        prefix, criteria = self._parse_locator(locator)
        driver = self._current_application()
        if prefix is None:
            if first_only:
                if criteria.startswith('//'):
                    return driver.find_element_by_xpath(criteria)
                return driver.find_element_by_accessibility_id(criteria)
            if criteria.startswith('//'):
                return driver.find_elements_by_xpath(criteria)
            return driver.find_elements_by_accessibility_id(criteria)
        if prefix == 'name':
            if first_only:
                return driver.find_element_by_name(criteria)
            return driver.find_elements_by_name(criteria)
        if prefix == 'class':
            if first_only:
                return driver.find_element_by_class_name(criteria)
            return driver.find_elements_by_class_name(criteria)
        if prefix == 'xpath':
            if first_only:
                return driver.find_element_by_xpath(criteria)
            return driver.find_elements_by_xpath(criteria)
        if prefix == 'accessibility_id':
            if first_only:
                return driver.find_element_by_accessibility_id(criteria)
            return driver.find_elements_by_accessibility_id(criteria)
        zoomba.fail("Element locator with prefix '" + prefix + "' is not supported")

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return prefix, criteria
