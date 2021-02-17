import itertools
from time import time
from selenium.webdriver.common.action_chains import ActionChains
from robot.libraries.BuiltIn import BuiltIn

SCREENSHOT_COUNTER = itertools.count()
zoomba = BuiltIn()


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
    """Takes a screenshot with a unique filename to be stored
    in Robot Framework compiled reports."""
    timestamp = time()
    filename = 'appium-screenshot-' + str(timestamp) + '-' + str(next(SCREENSHOT_COUNTER)) + '.png'
    return self.capture_page_screenshot(filename)


def wait_until_page_contains(self, text, timeout=None, error=None):
    """Internal version to avoid duplicate screenshots"""
    if not error:
        error = "Text '%s' did not appear in <TIMEOUT>" % text
    self._wait_until(timeout, error, self._is_text_present, text)


def drag_and_drop(self, source, target):
    """Drags the element found with the locator ``source`` to the element found with the
    locator ``target``."""
    source_element = self._element_find(source, True, True)
    target_element = self._element_find(target, True, True)
    actions = ActionChains(self._current_application())
    zoomba.log('Dragging source element "%s" to target element "%s".' % (source, target))
    actions.drag_and_drop(source_element, target_element).perform()


def drag_and_drop_by_offset(self, locator, x_offset=0, y_offset=0):
    """Drags the element found with ``locator`` to the given ``x_offset`` and ``y_offset``
    coordinates.
    """
    element = self._element_find(locator, True, True)
    actions = ActionChains(self._current_application())
    zoomba.log('Dragging element "%s" by offset (%s, %s).' % (locator, x_offset, y_offset))
    actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()
