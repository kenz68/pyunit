__author__ = 'quocle'
# run: py.test -v --junitxml results.xml test_open.py
import unittest

from module import module_command_cam_open
from controller import ctr_shell
from module import module_cam_open


class TestCamOpen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctr_shell.remove_file('result.xml')
        ctr_shell.open_miniterm()
    def setUp(self):
        # remove result file
        ctr_shell.remove_file('result')

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

    def test_open_a1_preview_sw(self):
        # open a1 sw preview
        ctr_shell.execute(module_command_cam_open.a1_preview_sw)
        # get log
        ctr_shell.adb_pull()
        # check log
        ctr_shell.print_file('result')
        # compare expect
        self.assertEqual('A1 OPEN', module_cam_open.a1_preview_sw)

if __name__ == '__main__':
    unittest.main()