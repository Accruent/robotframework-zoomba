import itertools
from robot.api.deco import keyword
from time import time

SCREENSHOT_COUNTER = itertools.count()


@keyword("Capture Page Screenshot")
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
