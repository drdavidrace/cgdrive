#!/usr/bin/env bash
echo "Start of tests"
#File utility Tests
echo "File utility tests"
python -m unittest -v test.test_file_utilities.suite
