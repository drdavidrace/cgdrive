'''
Tests for the file utilities.
This is fundamentally a command line set of tests, but a number of the 
internals are also tested.
'''
print("Start at Top")
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

    def file_name_creation_b(self):
        cur_dir = os.getcwd()
        full_dir = os.path.realpath(os.path.normpath(cur_dir))
        file_name = 'abc.txt'
        out_file_name = os.path.join(full_dir,file_name)
        create_state = create_file_name(cur_dir, file_name)
        self.assertEqual(create_state, out_file_name)

    def file_name_creation_c(self):
        cur_dir = '.'
        full_dir = os.path.realpath(os.path.normpath(cur_dir))
        file_name = 'abc.txt'
        out_file_name = os.path.join(full_dir,file_name)
        create_state = create_file_name(cur_dir, file_name)
        self.assertEqual(create_state, out_file_name)

    def file_name_creation_d(self):
        cur_dir = ''
        full_dir = os.path.realpath(os.path.normpath(cur_dir))
        file_name = 'abc.txt'
        out_file_name = os.path.join(full_dir,file_name)
        create_state = create_file_name(cur_dir, file_name)
        self.assertEqual(create_state, out_file_name)

    def file_name_creation_e(self):
        cur_dir = 'testDir'
        full_dir = os.path.join(os.getcwd(),cur_dir)
        file_name = 'abc.txt'
        out_file_name = os.path.join(full_dir,file_name)
        create_state = create_file_name(cur_dir, file_name)
        self.assertEqual(create_state, out_file_name)

    def file_name_creation_f(self):
        cur_dir = 'testDir'
        full_dir = os.path.join(os.getcwd(),cur_dir)
        file_name = 'abc.txt'
        out_file_name = os.path.join(full_dir,file_name)
        create_state = create_file_name(cur_dir, file_name, create_dir=True)
        dir_state = os.path.isdir(full_dir)
        os.rmdir(full_dir)
        dir_state_2 = os.path.isdir(full_dir)
        self.assertTrue(dir_state)
        self.assertFalse(dir_state_2)

class TestFileCreationManagement(unittest.TestCase):

    def file_creation_a(self):
        cur_dir = os.getcwd()
        cur_dir = os.path.normpath(cur_dir)
        file_name = 'abc.txt'
        out_file_name = os.path.join(cur_dir,file_name)
        create_state = create_file(file_name)
        isFile = os.path.isfile(out_file_name)
        self.assertEqual(create_state, out_file_name)
        self.assertTrue(isFile)
        os.remove(out_file_name)
        isFile = os.path.isfile(out_file_name)
        self.assertFalse(isFile)

    def dir_creation_a(self):
        cur_dir = os.getcwd()
        cur_dir = os.path.normpath(cur_dir)
        dir_name = 'testDir'
        out_dir_name = os.path.join(cur_dir,dir_name)
        create_state = create_dir(out_dir_name)
        isDir = os.path.isdir(create_state)
        self.assertEqual(create_state, out_dir_name)
        self.assertTrue(isDir)
        os.rmdir(out_dir_name)
        isDir = os.path.isdir(out_dir_name)
        self.assertFalse(isDir)


def suite_file_name():
    tests = ['file_name_creation_a', 'file_name_creation_b', 'file_name_creation_c',
    'file_name_creation_d', 'file_name_creation_e', 'file_name_creation_f']
    return unittest.TestSuite(map(TestFileNameManagement, tests))

def suite_file_creation():
    tests = ['file_creation_a', 'dir_creation_a']
    return unittest.TestSuite(map(TestFileCreationManagement, tests))
