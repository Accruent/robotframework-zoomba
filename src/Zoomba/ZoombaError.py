from robot.libraries.BuiltIn import BuiltIn

zoomba = BuiltIn()


class ZoombaError:
    def __init__(self, error=None, key=None, expected=None, actual=None, **kwargs):
        self.error = error
        self.key = key
        self.expected = expected
        self.actual = actual
        self.__dict__.update(kwargs)

    def __repr__(self):
        repr_obj = ""
        for attribute, value in self.__dict__.items():
            if value is not None:
                repr_obj += "\n" if repr_obj else ""
                repr_obj += f"{attribute.capitalize()}: {value}"
        return repr_obj

    def fail(self):
        zoomba.fail(self.__repr__())
