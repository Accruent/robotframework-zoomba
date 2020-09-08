import itertools
from time import time

SCREENSHOT_COUNTER = itertools.count()


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


def save_appium_screenshot(self):
    """Takes a screenshot with a unique filename to be stored in Robot Framework compiled reports."""
    timestamp = time()
    filename = 'appium-screenshot-' + str(timestamp) + '-' + str(next(SCREENSHOT_COUNTER)) + '.png'
    return self.capture_page_screenshot(filename)


def wait_until_page_contains(self, text, timeout=None, error=None):
    """Internal version to avoid duplicate screenshots"""
    if not error:
        error = "Text '%s' did not appear in <TIMEOUT>" % text
    self._wait_until(timeout, error, self._is_text_present, text)


def wait_until_page_contains_element(self, locator, timeout=None, error=None):
    """Internal version to avoid duplicate screenshots"""
    if not error:
        error = "Element '%s' did not appear in <TIMEOUT>" % locator
    self._wait_until(timeout, error, self._is_element_present, locator)


def wait_for_and_long_press(self, locator, duration=5000, timeout=None, error=None):
    """Wait for and long press the element identified by ``locator`` with optional duration.

    Fails if ``timeout`` expires before the element appears.

    ``error`` can be used to override the default error message.

    See `introduction` for details about locating elements."""
    self._wait_until_page_contains_element(locator, timeout, error)
    self.long_press(locator, duration)


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


def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
    """Waits until element specified with ``locator`` is enabled.

    Fails if ``timeout`` expires before the element appears.

    ``error`` can be used to override the default error message.

    See also `Wait Until Element Is Disabled`
    """
    self._wait_until_page_contains_element(locator, timeout, error)
    self.element_should_be_enabled(locator)


def wait_until_element_is_disabled(self, locator, timeout=None, error=None):
    """Waits until element specified with ``locator`` is disabled.

    Fails if ``timeout`` expires before the element appears.

    ``error`` can be used to override the default error message.

    See also `Wait Until Element Is Disabled`
    """
    self._wait_until_page_contains_element(locator, timeout, error)
    self.element_should_be_disabled(locator)
