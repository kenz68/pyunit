__author__ = 'quocle'
# run: py.test -v --junitxml results.xml test_open_hw.py
import unittest

from module import module_command_cam_open
from controller import ctr_shell
from module import module_cam_open
from util import util
from util import get_last_line

class TestCamOpenSW(unittest.TestCase):
   # @classmethod
    # def setUpClass(cls):
        # ctr_shell.execute('rm -rf result.xml')
        # ctr_shell.open_miniterm()
    # def setUp(self):
        # remove result file
        # ctr_shell.execute('rm -rf result.txt')

    def test_sc_open_sw_a1(self):
        # open a1 sw preview
        ctr_shell.execute(module_command_cam_open.sc_open_sw_a1)
        # get log
        # ctr_shell.adb_pull()
        # show log
        log = ctr_shell.get_log('result.txt')
        # get 50 last info
        info = get_last_line.get_n_last_lines('result.txt', 50)
        infos = util.get_last_elements(25, info)
        print info
        print infos
        self.assertTrue(util.items_in_list(module_cam_open.sc_open_sw_a1, infos))
    def test_sc_open_sw_b1(self):
        # open a1 sw preview
        ctr_shell.execute(module_command_cam_open.sc_open_sw_b1)
        # get log
        # ctr_shell.adb_pull()
        # show log
        log = ctr_shell.get_log('result.txt')
        # get 50 last info
        info = get_last_line.get_n_last_lines('result.txt', 50)
        infos = util.get_last_elements(25, info)
        print info
        print infos
        self.assertTrue(util.items_in_list(module_cam_open.sc_open_sw_b1, infos))
    def test_sc_open_sw_c1(self):
        # open a1 sw preview
        ctr_shell.execute(module_command_cam_open.sc_open_sw_c1)
        # get log
        # ctr_shell.adb_pull()
        # show log
        log = ctr_shell.get_log('result.txt')
        # get 50 last info
        info = get_last_line.get_n_last_lines('result.txt', 50)
        infos = util.get_last_elements(25, info)
        print info
        print infos
        self.assertTrue(util.items_in_list(module_cam_open.sc_open_sw_c1, infos))
if __name__ == '__main__':
    unittest.main()
