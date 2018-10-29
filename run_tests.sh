#!/usr/bin/env bash
echo "Start of tests"
#File utility Tests
echo "============================"
echo "File utility file name tests"
echo "============================"
python -m unittest -v test.test_file_utilities.suite_file_name
echo "============================"
echo "File utility file creation tests"
echo "============================"
python -m unittest -v test.test_file_utilities.suite_file_creation
