import itertools
from time import time
from appium.webdriver.common.touch_action import TouchAction
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


def drag_and_drop(self, source, target, delay=1500):
    """Drags the element found with the locator ``source`` to the element found with the
    locator ``target``.

    ``Delay`` (iOS Only): Delay between initial button press and dragging, defaults to 1500ms."""
    source_element = self._element_find(source, True, True)
    target_element = self._element_find(target, True, True)
    zoomba.log('Dragging source element "%s" to target element "%s".' % (source, target))
    actions = TouchAction(self._current_application())
    self._platform_dependant_press(actions, source_element, delay)
    actions.move_to(target_element)
    actions.release().perform()


def drag_and_drop_by_offset(self, locator, x_offset=0, y_offset=0, delay=1500):
    """Drags the element found with ``locator`` to the given ``x_offset`` and ``y_offset``
    coordinates.

    ``Delay`` (iOS Only): Delay between initial button press and dragging, defaults to 1500ms."""
    element = self._element_find(locator, True, True)
    zoomba.log('Dragging element "%s" by offset (%s, %s).' % (locator, x_offset, y_offset))
    x_center = element.location['x'] + element.size['width'] / 2
    y_center = element.location['y'] + element.size['height'] / 2
    actions = TouchAction(self._current_application())
    self._platform_dependant_press(actions, element, delay)
    actions.move_to(x=x_center + x_offset, y=y_center + y_offset)
    actions.release().perform()


def _platform_dependant_press(self, actions, element, delay):
    if self._is_ios():
        actions.long_press(element, duration=2000)
        actions.wait(delay)
    else:
        actions.press(element)
