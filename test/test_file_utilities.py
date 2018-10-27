'''
Tests for the file utilities
'''
#Test Imports
import unittest
#General Imports
import os
from pprint import pprint, pformat
#import file utilities
from utilities.file_utilities import *
#The Tests
class TestFileNameManagement(unittest.TestCase):
    def file_name_creation_a(self):
        cur_dir = os.getcwd()
        cur_dir = os.path.normpath(cur_dir)
        file_name = 'abc.txt'
        out_file_name = os.path.join(cur_dir,file_name)
        create_state = create_file_name(cur_dir, file_name)
        self.assertEqual(create_state, out_file_name)

    # def file_name_creation_2(self):
    #     cur_dir = os.getcwd()
    #     full_dir = os.path.normpath(cur_dir)
    #     file_name = 'abc.txt'
    #     out_file_name = os.path.join(full_dir,file_name)
    #     create_state = create_file_name(cur_dir, file_name)
    #     self.assertEqual(create_state, out_file_name)

if __name__ == '__main__':
    name_management = unittest.TestLoader().loadTestsFromTestCase(TestFileNameManagement)
    unittest.TextTestRunner(verbosity=2).run(name_management)
