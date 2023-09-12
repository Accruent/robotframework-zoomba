from robot.libraries.BuiltIn import BuiltIn

zoomba = BuiltIn()


class ZoombaError:
    def __init__(self, error=None, key=None, expected=None, actual=None, **kwargs):
        self.error = error
        self.key = key
        self.expected = expected
        self.actual = actual
        self.important = 'key'
        self.__dict__.update(kwargs)

    def __repr__(self):
        repr_obj = ""
        if bool(self.expected) ^ bool(self.actual):
            self.expected = str(self.expected)
            self.actual = str(self.actual)
        for attribute, value in self.__dict__.items():
            if value is None:
                continue
            if attribute == "important":
                continue
            repr_obj += "\n" if repr_obj else ""
            repr_obj += "------------------\n" if attribute == self.important else ""
            attribute = attribute.replace('_', ' ')
            repr_obj += f"{attribute.title() if attribute[0].islower() else attribute}: {value}"
        return repr_obj

    def __eq__(self, other):
        if hasattr(other, "__dict__"):
            return self.__dict__ == other.__dict__
        return self.__repr__() == other

    def fail(self):
        zoomba.fail(self.__repr__())
