# Taken from robotframework-appiumlibrary

import logging
import sys
import unittest
import mock
import base64

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)


class WebdriverRemoteMock(mock.Mock, unittest.TestCase):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=None):
        super(WebdriverRemoteMock, self).__init__()
        self._appiumUrl = command_executor
        self._desCapa = desired_capabilities
        self._dead = False
        self._myData = ''
        for key in desired_capabilities:
            self.assertNotEqual(desired_capabilities[key], None, 'Null value in desired capabilities')

    def _get_child_mock(self, **kwargs):
        return mock.Mock(**kwargs)

    def quit(self):
        self._dead = True

    def lock(self):
        if self._dead:
            raise RuntimeError('Application has been closed')

    def pull_file(self, decode=False):
        file = self._myData
        if decode:
            file = base64.b64decode(file)
        return file

    def push_file(self, data, encode=False):
        self._myData = base64.b64decode(data) if encode else data

    def find_element_by_name(self, *args):
        return Window


class Window:
    def get_attribute(self, *args):
        return 12345
