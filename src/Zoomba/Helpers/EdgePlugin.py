import importlib
from selenium import webdriver
from SeleniumLibrary import BrowserManagementKeywords
from SeleniumLibrary.utils import is_truthy, is_falsy
from SeleniumLibrary.keywords.webdrivertools import WebDriverCreator, SeleniumOptions
from msedge.selenium_tools import Edge as EdgePluginDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .chromeOptions import ChromiumOptions
from robot.api.deco import keyword


class EdgePlugin(BrowserManagementKeywords):
    """
    This plugin is used to adapt SeleniumLibrary to run Edge browser
    (even chromium based version) with stable selenium version (3.141).
    It uses special msedge-selenium-tools
    that allows driving the new Microsoft Edge (Chromium) browser
    and use the latest functionality with no need to update to the alpha 4th selenium version.
    """
    def __init__(self, ctx):
        BrowserManagementKeywords.__init__(self, ctx)
        self._webdriver_creator = _EdgePluginWebDriverCreator(self.log_dir)

    @keyword
    def get_edge_options(self):
        return Options()


class _EdgePluginWebDriverCreator(WebDriverCreator):
    def __init__(self, log_dir):
        super().__init__(log_dir)
        self.log_dir = log_dir
        self.selenium_options = _EdgePluginSeleniumOptions()

    def create_edge(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                    executable_path='msedgedriver.exe'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.EDGE.copy()
            desired_capabilities = self._remote_capabilities_resolver(
                desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(EdgePluginDriver)
        return EdgePluginDriver(options=options,
                                service_log_path=service_log_path,
                                executable_path=executable_path,
                                **desired_capabilities)


class _EdgePluginSeleniumOptions(SeleniumOptions):
    def _import_options(self, browser):
        if browser == 'edge':
            options = importlib.import_module('msedge.selenium_tools.options')
            return options.Options
        return super(_EdgePluginSeleniumOptions, self)._import_options(browser)


# Pulled from selenium 4 beta for now as AppiumLibrary is not compatible with it yet

class Options(ChromiumOptions):
    KEY = "ms:edgeOptions"

    def __init__(self):
        super(Options, self).__init__()
        self._use_chromium = True
        self._use_webview = False

    @property
    def use_chromium(self) -> bool:
        return self._use_chromium

    @use_chromium.setter
    def use_chromium(self, value: bool):
        self._use_chromium = bool(value)

    @property
    def use_webview(self) -> bool:
        return self._use_webview

    @use_webview.setter
    def use_webview(self, value: bool):
        self._use_webview = bool(value)

    def to_capabilities(self) -> dict:
        """
        Creates a capabilities with all the options that have been set and
        :Returns: A dictionary with everything
        """
        caps = self._caps

        if self._use_chromium:
            caps = super(Options, self).to_capabilities()
            if self._use_webview:
                caps['browserName'] = 'webview2'
        else:
            caps['platform'] = 'windows'

        caps['ms:edgeChromium'] = self._use_chromium
        return caps

    @property
    def default_capabilities(self) -> dict:
        return DesiredCapabilities.EDGE.copy()