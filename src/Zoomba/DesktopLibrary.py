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
    """

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
    def wait_for_and_clear_text(self, locator):
        """Wait for and then clear the text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator)
        self.clear_text(locator)

    @keyword("Wait For And Click Element")
    def wait_for_and_click_element(self, locator):
        """Wait for and click the element identified by `locator`.

        Key attributes for arbitrary elements are `index` and `name`. See
        `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator)
        self.click_element(locator)

    @keyword("Wait For And Click Text")
    def wait_for_and_click_text(self, text, exact_match=False):
        """Wait for and click text identified by ``text``.

        By default tries to click first text involves given ``text``, if you would
        like to click exactly matching text, then set ``exact_match`` to `True`.

        If there are multiple use  of ``text`` and you do not want first one,
        use `locator` with `Get Web Elements` instead.

        """
        self.wait_until_page_contains_text(text)
        self.click_text(text, exact_match)

    @keyword("Wait For And Input Password")
    def wait_for_and_input_password(self, locator, text):
        """Wait for and type the given password into the text field identified by `locator`.

        The difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self.wait_until_page_contains_element(locator)
        self.input_password(locator, text)

    @keyword("Wait For And Input Text")
    def wait_for_and_input_text(self, locator, text):
        """Wait for and type the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self.wait_until_page_contains_element(locator)
        self.input_text(locator, text)

    @keyword("Wait For And Long Press")
    def wait_for_and_long_press(self, locator, duration=10000):
        """Wait for and long press the element with optional duration """
        self.wait_until_page_contains_element(locator)
        self.long_press(locator, duration)

