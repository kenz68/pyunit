__author__ = 'quocle'
import unittest
from controller import ctr_shell

class TestCamOpen(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        ctr_shell.execute('adb shell')
        ctr_shell.execute('ls -l')
        self.assertEqual(s.split(), ['hello', 'world'])

if __name__ == '__main__':
    unittest.main()