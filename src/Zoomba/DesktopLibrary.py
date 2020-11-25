import os
import subprocess
import importlib
from AppiumLibrary import AppiumLibrary
from appium import webdriver
from psutil import Process, NoSuchProcess
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions

from time import sleep, time
from robot import utils

try:
    AppiumCommon = importlib.import_module('Helpers.AppiumCommon', package='Helpers')
except ModuleNotFoundError:
    AppiumCommon = importlib.import_module('.Helpers.AppiumCommon', package='Zoomba')

zoomba = BuiltIn()


class WinAppDriver:
    def __init__(self, driver_path=""):
        self.process = None
        self.driver_path = driver_path

    def set_up_driver(self, path=None):
        if path is None:
            path = self.driver_path
        try:
            stdout = open(os.devnull, 'w')
            self.process = subprocess.Popen([path], stdout=stdout)
            stdout.close()
        except Exception:
            self.process = None
            stdout.close()

    def tear_down_driver(self):
        try:
            process = Process(self.process.pid)
            for pro in process.children(recursive=True):
                pro.kill()
                pro.wait()
            self.process.kill()
            self.process.wait()
            self.process = None
        except (NoSuchProcess, AttributeError):
            subprocess.call("C:/Windows/system32/taskkill.exe /f /im WinAppDriver.exe", shell=False)
            self.process = None


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
    |       image        |                N/A                 | Click Element `|` image=file.png                  |

    The ``image`` locator strategy can only be used with Appium v1.18.0 or higher.

    Example tests using the windows calculator are located in the tests directory.

    = Use of Wait Keywords =

    When using a modern Windows application there should be no issue with using the 'Wait For And' keywords. However if
    you are using an older WinForm, Win32, or a larger application it may be necessary to simply use the non-waiting
    version of keywords. Then you would simply add your waits in manually where necessary using something like
    ``Wait Until Page Contains`` or ``Wait Until Page Contains Element``.
    """

    def __init__(self, timeout=5, run_on_failure='Save Appium Screenshot',
                 driver_path="C:\\Program Files (x86)\\Windows Application Driver\\WinAppDriver.exe"):
        """DesktopLibrary can be imported with optional arguments.

        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.

        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a DesktopLibrary keyword fails.
        By default `Save Appium Screenshot` will be used to take a screenshot of the current page.
        Using the value ``No Operation`` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        ``driver_path`` is the path to the WinAppDriver.exe file.

        Examples:
        | Library | DesktopLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | DesktopLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        | Library | DesktopLibrary | timeout=10 | driver_path="C:/WinAppDriver.exe" | # Sets a new path for the WinAppDriver                               |
        """
        self.winappdriver = WinAppDriver(driver_path)
        super().__init__(timeout, run_on_failure)

    def get_keyword_names(self):
        """
        This function restricts the keywords used in the library. This is to prevent incompatible
        keywords from imported libraries from being referenced and used.
        """
        return [
            'maximize_window', 'open_application', 'wait_for_and_clear_text',
            'wait_for_and_click_element', 'wait_for_and_input_password', 'wait_for_and_input_text',
            'wait_for_and_long_press', 'wait_until_element_contains',
            'wait_until_element_does_not_contain', 'wait_until_element_is_enabled',
            'wait_until_element_is_disabled', 'switch_application_by_name', 'mouse_over_element',
            'wait_for_and_mouse_over_element', 'mouse_over_and_click_element',
            'wait_for_and_mouse_over_and_click_element', 'click_a_point', 'context_click_a_point',
            'mouse_over_and_context_click_element', 'mouse_over_by_offset', 'drag_and_drop',
            'drag_and_drop_by_offset', 'send_keys', 'send_keys_to_element',
            'capture_page_screenshot', 'save_appium_screenshot', 'select_element_from_combobox',
            'driver_setup', 'driver_teardown', 'select_elements_from_menu',
            'select_elements_from_context_menu', 'drag_and_drop_by_touch',
            'drag_and_drop_by_touch_offset', 'wait_for_and_tap', 'wait_for_and_double_tap',
            'double_tap', 'flick', 'flick_from_element', 'scroll', 'scroll_from_element',
            'wait_for_and_flick_from_element', 'wait_for_and_scroll_from_element',
            # External Libraries
            'clear_text', 'click_button', 'click_element', 'close_all_applications',
            'close_application', 'element_attribute_should_match', 'element_should_be_disabled',
            "element_should_be_enabled", 'element_should_be_visible', 'element_should_contain_text',
            'element_should_not_contain_text', 'element_text_should_be', 'get_appium_sessionId',
            'get_appium_timeout', 'get_capability', 'get_element_attribute', 'get_element_location',
            'get_element_size', 'get_webelement', 'get_webelements', 'get_window_height',
            'get_window_width', 'input_password', 'input_text', 'launch_application', 'log_source',
            'long_press', 'page_should_contain_element', 'page_should_contain_text',
            'page_should_not_contain_element', 'page_should_not_contain_text', 'quit_application',
            'register_keyword_to_run_on_failure', 'set_appium_timeout', 'switch_application',
            'text_should_be_visible', 'wait_until_element_is_visible', 'wait_until_page_contains',
            'wait_until_page_contains_element', 'wait_until_page_does_not_contain',
            'wait_until_page_does_not_contain_element', 'get_matching_xpath_count',
            'xpath_should_match_x_times', 'tap'
        ]

    @keyword("Driver Setup")
    def driver_setup(self, path=None):
        """Starts the WinAppDriver.

        ``path`` can be provided if your winappdriver installation is not in the default path of
        ``C:/Program Files (x86)/Windows Application Driver/WinAppDriver.exe``.

        Not to be used with Appium."""
        self.winappdriver.set_up_driver(path)

    @keyword("Driver Teardown")
    def driver_teardown(self):
        """Stops the WinAppDriver.

        Not to be used with Appium."""
        self.winappdriver.tear_down_driver()

    @keyword("Maximize Window")
    def maximize_window(self):
        """Maximizes the current application window."""
        self._current_application().maximize_window()
        return True

    @keyword("Open Application")
    def open_application(self, remote_url, alias=None, window_name=None, splash_delay=0,
                         exact_match=True, **kwargs):
        """Opens a new application to given Appium server.
        If your application has a splash screen please supply the window name of the final window that will appear.
        For the capabilities of appium server and Windows please check http://appium.io/docs/en/drivers/windows

        | *Option*            | *Man.* | *Description*                                                        |
        | remote_url          | Yes    | Appium server url                                                    |
        | alias               | No     | Alias                                                                |
        | window_name         | No     | Window name you wish to attach, usually after a splash screen        |
        | splash_delay        | No     | Delay used when waiting for a splash screen to load, in seconds      |
        | exact_match         | No     | Set to False if window_name does not need to match exactly           |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          |
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          | window_name=MyApplication          | splash_delay=5          |
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | app=your.app          | window_name=MyApplication          | exact_match=False       |

        A session for the root desktop will also be opened and can be switched to by running the following:
        | Switch Application | Desktop         |
        """
        desired_caps = kwargs

        if window_name:
            # If the app has a splash screen we need to supply the window_name of the final window.
            # This code path will start the application and then attach to the correct window via
            # the window_name.
            self._info('Opening application "%s"' % desired_caps['app'])
            subprocess.Popen(desired_caps['app'])
            if splash_delay > 0:
                self._info('Waiting %s seconds for splash screen' % splash_delay)
                sleep(splash_delay)
            return self.switch_application_by_name(remote_url, alias=alias, window_name=window_name,
                                                   exact_match=exact_match, **kwargs)
        # global application
        self._open_desktop_session(remote_url)
        if "platformName" not in desired_caps:
            desired_caps["platformName"] = "Windows"
        application = webdriver.Remote(str(remote_url), desired_caps)
        self._debug('Opened application with session id %s' % application.session_id)
        return self._cache.register(application, alias)

    @keyword("Switch Application By Name")
    def switch_application_by_name(self, remote_url, window_name, alias=None, timeout=5,
                                   exact_match=True, **kwargs):
        """Switches to a currently opened window by ``window_name``.
        For the capabilities of appium server and Windows,
        Please check http://appium.io/docs/en/drivers/windows
        | *Option*            | *Man.* | *Description*                         |
        | remote_url          | Yes    | Appium server url                     |
        | window_name         | Yes    | Window name you wish to attach        |
        | alias               | No     | alias                                 |
        | timeout             | No     | timeout to connect                    |
        | exact_match         | No     | Set to False if window_name does not need to match exactly       |

        Examples:
        | Switch Application By Name | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=Windows            | deviceName=Windows           | window_name=MyApplication         |
        | Switch Application By Name | http://localhost:4723/wd/hub | window_name=MyApp    |  exact_match=False  |

        A session for the root desktop will also be opened and can be switched to by running the following:
        | Switch Application | Desktop         |
        """
        desired_caps = kwargs
        desktop_session = self._open_desktop_session(remote_url)
        window_xpath = '//Window[contains(@Name, "' + window_name + '")]'
        try:
            if exact_match:
                window = desktop_session.find_element_by_name(window_name)
            else:
                window = desktop_session.find_element_by_xpath(window_xpath)
            self._debug('Window_name "%s" found.' % window_name)
            window = hex(int(window.get_attribute("NativeWindowHandle")))
        except Exception:
            try:
                error = "Window '%s' did not appear in <TIMEOUT>" % window_name
                if exact_match:
                    self._wait_until(timeout, error, desktop_session.find_element_by_name,
                                     window_name)
                    window = desktop_session.find_element_by_name(window_name)
                else:
                    self._wait_until(timeout, error, desktop_session.find_element_by_xpath,
                                     window_xpath)
                    window = desktop_session.find_element_by_xpath(window_xpath)
                self._debug('Window_name "%s" found.' % window_name)
                window = hex(int(window.get_attribute("NativeWindowHandle")))
            except Exception as e:
                self._debug('Closing desktop session.')
                zoomba.fail(
                    'Error finding window "' + window_name + '" in the desktop session. '
                    'Is it a top level window handle?' + '. \n' + str(e))
        if "app" in desired_caps:
            del desired_caps["app"]
        if "platformName" not in desired_caps:
            desired_caps["platformName"] = "Windows"
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

        This keyword works while `Open Application` has a test running. This is good practice to
        `Launch Application` and `Quit Application` between test cases. As Suite Setup is
        `Open Application`, `Test Setup` can be used to `Launch Application`

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
        self._current_application().launch_app()

    @keyword("Wait For And Clear Text")
    def wait_for_and_clear_text(self, locator, timeout=None, error=None):
        """Wait for and then clear the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.clear_text(locator)

    def click_element(self, locator):
        """Click element identified by `locator`.

        Supported prefixes: ``accessibility_id``, ``name``, ``class``, ``xpath``, and ``image``

        The ``image`` locator strategy can only be used with Appium v1.18.0 and newer.

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
        
        Use `Wait For And Mouse Over And Click Element` if this keyword gives issues in the
        application."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.click_element(locator)

    @keyword("Wait For And Input Password")
    def wait_for_and_input_password(self, locator, text, timeout=None, error=None):
        """Wait for and type the given password into the text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        The difference between this keyword and `Wait For And Input Text` is that this keyword
        does not log the given password. See `introduction` for details about locating elements."""
        AppiumCommon.wait_for_and_input_password(self, locator, text, timeout, error)

    @keyword("Wait For And Input Text")
    def wait_for_and_input_text(self, locator, text, timeout=None, error=None):
        """Wait for and type the given ``locator`` into text field identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        AppiumCommon.wait_for_and_input_text(self, locator, text, timeout, error)

    @keyword("Wait For And Long Press")
    def wait_for_and_long_press(self, locator, duration=10000, timeout=None, error=None):
        """Wait for and long press the element identified by ``locator`` with optional duration.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        AppiumCommon.wait_for_and_long_press(self, locator, duration, timeout, error)

    @keyword("Wait Until Element Contains")
    def wait_until_element_contains(self, locator, text, timeout=None, error=None):
        """Waits until element specified with ``locator`` contains ``text``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        """
        AppiumCommon.wait_until_element_contains(self, locator, text, timeout, error)

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
        AppiumCommon.wait_until_element_does_not_contain(self, locator, text, timeout, error)

    @keyword("Wait Until Element Is Enabled")
    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is enabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        AppiumCommon.wait_until_element_is_enabled(self, locator, timeout, error)

    @keyword("Wait Until Element Is Disabled")
    def wait_until_element_is_disabled(self, locator, timeout=None, error=None):
        """Waits until element specified with ``locator`` is disabled.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See also `Wait Until Element Is Disabled`
        """
        AppiumCommon.wait_until_element_is_disabled(self, locator, timeout, error)

    @keyword("Mouse Over Element")
    def mouse_over_element(self, locator, x_offset=0, y_offset=0):
        """Moves the mouse over the given ``locator``.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        element = self._element_find(locator, True, True)
        actions = ActionChains(self._current_application())
        self._move_to_element(actions, element, x_offset, y_offset)
        actions.perform()

    @keyword("Wait For And Mouse Over Element")
    def wait_for_and_mouse_over_element(self, locator, timeout=None, error=None, x_offset=0,
                                        y_offset=0):
        """Waits for and moves the mouse over the given ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        self._wait_until_page_contains_element(locator, timeout, error)
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
    def wait_for_and_mouse_over_and_click_element(self, locator, timeout=None, error=None,
                                                  double_click=False, x_offset=0, y_offset=0):
        """Waits for, moves the mouse over, and clicks the given ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        ``double_click`` can be used to click twice.

        ``x_offset`` and ``y_offset`` can be used to move to a specific coordinate.
        """
        self._wait_until_page_contains_element(locator, timeout, error)
        self.mouse_over_and_click_element(locator, double_click, x_offset, y_offset)

    @keyword("Mouse Over By Offset")
    def mouse_over_by_offset(self, x_offset=0, y_offset=0):
        """Moves the mouse from its current location by the given ``x_offset`` and ``y_offset``.
        """
        actions = ActionChains(self._current_application())
        actions.move_by_offset(x_offset, y_offset)
        self._info('Moving mouse from current location with an '
                   'offset of (%s,%s).' % (x_offset, y_offset))
        actions.perform()

    @keyword("Click A Point")
    def click_a_point(self, x_offset=0, y_offset=0, double_click=False):
        """Clicks the current mouse location.

        ``x_offset`` and ``y_offset`` can be applied to give an offset.

        ``double_click`` can be used to click twice.
        """
        actions = ActionChains(self._current_application())
        if x_offset != 0 or y_offset != 0:
            actions.move_by_offset(x_offset, y_offset)
        self._info("Clicking on current mouse position with an "
                   "offset of (%s,%s)." % (x_offset, y_offset))
        if double_click:
            actions.double_click().perform()
        else:
            actions.click().perform()

    @keyword("Context Click A Point")
    def context_click_a_point(self, x_offset=0, y_offset=0):
        """Right-clicks the current mouse location.

        ``x_offset`` and ``y_offset`` can be applied to give an offset.
        """
        actions = ActionChains(self._current_application())
        if x_offset != 0 or y_offset != 0:
            actions.move_by_offset(x_offset, y_offset)
        self._info("Right-clicking on current mouse position with an "
                   "offset of (%s,%s)." % (x_offset, y_offset))
        actions.context_click().perform()

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

    @keyword("Send Keys")
    def send_keys(self, *argv):
        """Sends the desired keys in ``argv``.

        A list of special key codes can be found
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html|here]

        Note that when sending in a modifier key (Ctrl, Alt, Shift) you will need to send the key
        again to release it.
        |  Send Keys  |      a              |    b   |
        |  Send Keys  |      \\ue00        |    p    |    \\ue00     |
        """
        actions = ActionChains(self._current_application())
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

        Note that when sending in a modifier key (Ctrl, Alt, Shift) you will need to send the key
        again to release it.
        |  Send Keys To Element  |     locator    |      a              |    b   |
        |  Send Keys To Element  |     locator    |      \\ue00        |    p    |    \\ue00     |
        """
        actions = ActionChains(self._current_application())
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
        the background color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.

        See `Save Appium Screenshot` for a screenshot that will be unique across reports
        """
        return AppiumCommon.capture_page_screenshot(self, filename)

    @keyword("Save Appium Screenshot")
    def save_appium_screenshot(self):
        """Takes a screenshot with a unique filename to be stored in Robot Framework compiled
        reports."""
        return AppiumCommon.save_appium_screenshot(self)

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
            try:
                self._element_find(element_locator, True, True)
                self.click_element(element_locator)
            except NoSuchElementException:
                self._wait_until_page_contains_element(element_locator, self.get_appium_timeout())
                self.click_element(element_locator)
        except ValueError:
            original_index = self._cache.current_index
            self.switch_application('Desktop')
            try:
                self.click_element(element_locator)
            except NoSuchElementException:
                self._wait_until_page_contains_element(element_locator, self.get_appium_timeout())
                self.click_element(element_locator)
            self.switch_application(original_index)

    @keyword("Select Elements From Menu")
    def select_elements_from_menu(self, *args):
        """Selects N number of elements in the order they are given. This is useful for working
        though a nested menu listing of elements.

        On failure this keyword will attempt to select the elements from the desktop session due to
        the nature of some pop-out menus in Windows."""
        count = 0
        try:
            for each in args:
                self.click_element(each)
                count += 1
        except NoSuchElementException:
            original_index = self._cache.current_index
            self.switch_application('Desktop')
            for each in args[count:]:
                try:
                    self.click_element(each)
                except NoSuchElementException:
                    self._wait_until_page_contains_element(each, self.get_appium_timeout())
                    self.click_element(each)
                count += 1
            self.switch_application(original_index)

    @keyword("Select Elements From Context Menu")
    def select_elements_from_context_menu(self, *args):
        """Context clicks the first element and then selects N number of elements in the order they
        are given. This is useful for working though a nested context menu listing of elements.

        On failure this keyword will attempt to select the elements from the desktop session due to
        the nature of some pop-out menus in Windows."""
        count = 0
        try:
            for each in args:
                if count == 0:
                    self.mouse_over_and_context_click_element(each)
                else:
                    self.click_element(each)
                count += 1
        except NoSuchElementException:
            original_index = self._cache.current_index
            self.switch_application('Desktop')
            for each in args[count:]:
                try:
                    if count == 0:
                        self.mouse_over_and_context_click_element(each)
                    else:
                        self.click_element(each)
                except NoSuchElementException:
                    if count == 0:
                        self._wait_until_page_contains_element(each, self.get_appium_timeout())
                        self.mouse_over_and_context_click_element(each)
                    else:
                        self._wait_until_page_contains_element(each, self.get_appium_timeout())
                        self.click_element(each)
                count += 1
            self.switch_application(original_index)

    @keyword("Drag And Drop by Touch")
    def drag_and_drop_by_touch(self, source, target):
        """Drags the element found with the locator ``source`` to the element found with the
        locator ``target`` using touch actions."""
        source_element = self._element_find(source, True, True)
        target_element = self._element_find(target, True, True)
        actions = TouchActions(self._current_application())
        source_x_center = source_element.location.get('x') + (source_element.size.get('width') / 2)
        source_y_center = source_element.location.get('y') + (source_element.size.get('height') / 2)
        target_x_center = target_element.location.get('x') + (target_element.size.get('width') / 2)
        target_y_center = target_element.location.get('y') + (target_element.size.get('height') / 2)
        actions.tap_and_hold(source_x_center, source_y_center).release(target_x_center, target_y_center).perform()

    @keyword("Drag And Drop by Touch Offset")
    def drag_and_drop_by_touch_offset(self, locator, x_offset=0, y_offset=0):
        """Drags the element found with ``locator `` to the given ``x_offset`` and ``y_offset``
        coordinates using touch actions."""
        source_element = self._element_find(locator, True, True)
        actions = TouchActions(self._current_application())
        source_x_center = source_element.location.get('x') + (source_element.size.get('width') / 2)
        source_y_center = source_element.location.get('y') + (source_element.size.get('height') / 2)
        actions.tap_and_hold(source_x_center, source_y_center).release(x_offset, y_offset).perform()

    @keyword("Double Tap")
    def double_tap(self, locator):
        """ Double tap element identified by ``locator``."""
        element = self._element_find(locator, True, True)
        action = TouchActions(self._current_application())
        action.double_tap(element).perform()

    @keyword("Wait For And Tap")
    def wait_for_and_tap(self, locator, timeout=None, error=None):
        """Wait for and tap the element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.tap(locator)

    @keyword("Wait For And Double Tap")
    def wait_for_and_double_tap(self, locator, timeout=None, error=None):
        """Wait for and double tap the element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.double_tap(locator)

    @keyword("Flick")
    def flick(self, x_speed, y_speed):
        """ Flicks from current position.

         ``x_speed`` is the X speed in pixels per second.

         ``y_speed`` is the Y speed in pixels per second."""
        action = TouchActions(self._current_application())
        action.flick(x_speed, y_speed).perform()

    @keyword("Flick From Element")
    def flick_from_element(self, locator, x_offset, y_offset, speed):
        """ Flicks starting at ``locator``.

        ``x_offset`` is X offset to flick to.

        ``y_offset`` is Y offset to flick to.

        ``speed`` is Pixels per second to flick."""
        element = self._element_find(locator, True, True)
        action = TouchActions(self._current_application())
        action.flick_element(element, x_offset, y_offset, speed).perform()

    @keyword("Wait For And Flick From Element")
    def wait_for_and_flick_from_element(self, locator, x_offset, y_offset, speed,
                                        timeout=None, error=None):
        """Wait for and flick from element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.flick_from_element(locator, x_offset, y_offset, speed)

    @keyword("Scroll")
    def scroll(self, x_offset, y_offset):
        """ Scrolls from current position.

         ``x_offset`` is the X offset to scroll to.

         ``y_offset`` is the Y offset to scroll to."""
        action = TouchActions(self._current_application())
        action.scroll(x_offset, y_offset).perform()

    @keyword("Scroll From Element")
    def scroll_from_element(self, locator, x_offset, y_offset):
        """ Scrolls starting from ``locator``.

         ``x_offset`` is the X offset to scroll to.

         ``y_offset`` is the Y offset to scroll to."""
        element = self._element_find(locator, True, True)
        action = TouchActions(self._current_application())
        action.scroll_from_element(element, x_offset, y_offset).perform()

    @keyword("Wait For And Scroll From Element")
    def wait_for_and_scroll_from_element(self, locator, x_offset, y_offset,
                                         timeout=None, error=None):
        """Wait for and scroll from element identified by ``locator``.

        Fails if ``timeout`` expires before the element appears.

        ``error`` can be used to override the default error message.

        See `introduction` for details about locating elements."""
        self._wait_until_page_contains_element(locator, timeout, error)
        self.scroll_from_element(locator, x_offset, y_offset)

    # Private
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
            desktop_capabilities = dict({"app": "Root", "platformName": "Windows",
                                         "deviceName": "Windows", "newCommandTimeout": 3600})
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
        if prefix == 'image':
            try:
                if first_only:
                    return driver.find_element_by_image(criteria)
                return driver.find_elements_by_image(criteria)
            except InvalidSelectorException:
                zoomba.fail("Selecting by image is only available when using Appium "
                            "v1.18.0 or higher")
        zoomba.fail("Element locator with prefix '" + prefix + "' is not supported")

    def _is_element_present(self, locator):
        prefix, criteria = self._parse_locator(locator)
        driver = self._current_application()
        if prefix is None:
            if criteria.startswith('//'):
                return len(driver.find_elements_by_xpath(criteria)) > 0
            return len(driver.find_elements_by_accessibility_id(criteria)) > 0
        if prefix == 'name':
            return len(driver.find_elements_by_name(criteria)) > 0
        if prefix == 'class':
            return len(driver.find_elements_by_class_name(criteria)) > 0
        if prefix == 'xpath':
            return len(driver.find_elements_by_xpath(criteria)) > 0
        if prefix == 'accessibility_id':
            return len(driver.find_elements_by_accessibility_id(criteria)) > 0
        if prefix == 'image':
            try:
                return len(driver.find_elements_by_image(criteria)) > 0
            except InvalidSelectorException:
                zoomba.fail("Selecting by image is only available when using Appium v1.18.0 or higher")
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

    def _wait_until_page_contains(self, text, timeout=None, error=None):
        """Internal version to avoid duplicate screenshots"""
        AppiumCommon.wait_until_page_contains(self, text, timeout, error)

    def _wait_until_page_contains_element(self, locator, timeout=None, error=None):
        """Internal version to avoid duplicate screenshots"""
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)

    # Overrides to prevent expensive log_source call
    def _wait_until_no_error(self, timeout, wait_func, *args):
        timeout = utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        max_time = time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return
            if time() > max_time:
                raise AssertionError(timeout_error)
            sleep(0.2)
