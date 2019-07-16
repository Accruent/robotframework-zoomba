from AppiumLibrary import AppiumLibrary
from appium import webdriver
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

zoomba = BuiltIn()


class DesktopLibrary(AppiumLibrary):
    """Zoomba Desktop Library
        This class is the base Library used to generate automated Desktop Tests in the Robot Automation Framework using
        Appium. This Library uses and extends the robotframework-appiumlibrary.
    """

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
        try:
            desired_caps = kwargs
            # global application
            application = webdriver.Remote(str(remote_url), desired_caps)
        except:
            if window_name:
                desktop_capabilities = dict()
                desktop_capabilities["app"] = "Root"
                desktop_capabilities["platformName"] = "Windows"
                desktop_capabilities["deviceName"] = "WindowsPC"
                desktop_session = webdriver.Remote(str(remote_url), desktop_capabilities)
                window = desktop_session.find_element_by_name(window_name)
                window = hex(int(window.get_attribute("NativeWindowHandle")))
                try:
                    if desired_caps["app"]:
                        del desired_caps["app"]
                except:
                    pass
                desired_caps["appTopLevelWindow"] = window
                # global application
                application = webdriver.Remote(str(remote_url), desired_caps)

        self._debug('Opened application with session id %s' % application.session_id)

        return self._cache.register(application, alias)

    @keyword("Maximize Window")
    def maximize_window(self):
        """Maximizes the current application window.

        Windows Only.
        """
        driver = self._current_application()
        driver.maximize_window()
        return True
