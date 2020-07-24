from .ReactSelect import ReactSelect
from SeleniumLibrary.base import LibraryComponent
from SeleniumLibrary.utils import is_truthy


class ReactHelper(LibraryComponent):
    def __init__(self, gui_library_instance):
        #seleniumlib = BuiltIn().get_library_instance('Zoomba.GUILibrary')  # ToDo: Remove after confirming keyword works.
        self.seleniumlib = gui_library_instance
        super().__init__(self.seleniumlib)

    def get_react_list_items(self, locator, values=False):
        options = self._get_options(locator, 'div')
        if is_truthy(values):
            return self._get_values(options)
        else:
            return self._get_labels(options)

    def select_from_react_list_by_label(self, locator, label):
        """
        Selects option from selection list 'locator' by 'label'.
        :param locator: string - locator of element
        :param label: sting - label to select
        """
        self.info(f'Selecting option from selection list {locator} by label {label}')
        select = self._get_select_list(locator)
        select.select_by_visible_text(label)

    def _format_selection(self, labels, values):
        return ' | '.join('%s (%s)' % (label, value)
                          for label, value in zip(labels, values))

    def _get_select_list(self, locator, tag='div'):
        el = self.find_element(locator, tag=tag)
        return ReactSelect(el)

    def _get_options(self, locator, tag):
        return self._get_select_list(locator, tag).options

    def _get_labels(self, options):
        return [opt.text for opt in options]

    def _get_values(self, options):
        return [opt.get_attibute('value') for opt in options]
