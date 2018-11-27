"""
This module tests the module Time Manager.
"""
import unittest

from time_manager import check_root_privileges, get_current_time


class TimeManagerTest(unittest.TestCase):


    def test_check_root_privileges(self):
        uid = check_root_privileges()
        self.assertIsInstance(uid,bool)

    def test_get_current_time(self):
        current_tine = get_current_time()
        self.assertIsInstance(current_tine,str)

if __name__ == '__main__':
    unittest.main()
