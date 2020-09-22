import importlib
from selenium import webdriver
from SeleniumLibrary import BrowserManagementKeywords
from SeleniumLibrary.utils import is_truthy, is_falsy
from SeleniumLibrary.keywords.webdrivertools import WebDriverCreator, SeleniumOptions
from msedge.selenium_tools import Edge as EdgePluginDriver


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
