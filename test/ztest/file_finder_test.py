#!/usr/bin/env python3

import os
import unittest

from src import file_finder


class TestFileFinder(unittest.TestCase):
    def test_corner_cases(self):
        with self.assertRaises(FileNotFoundError):
            file_finder.findVariablesInFile("/nonexistent/path")

        with self.assertRaises(FileNotFoundError):
            file_finder.findVariablesInDir("/nonexistent/path")

    def test_findVariablesInFile(self):
        got = file_finder.findVariablesInFile(__file__)

        this_variable = [t for t in got if t[2] == "this_variable"][0]
        filepath, function_or_class, variable_name, is_local = this_variable

        self.assertEqual(__file__, filepath)
        self.assertEqual(function_or_class.name, "test_findVariablesInFile")

        self.assertTrue(is_local)

    def test_findVariablesInDir(self):
        got = file_finder.findVariablesInDir(os.path.dirname(__file__))

        that_variable = [t for t in got if t[2] == "that_variable"][0]
        filepath, function_or_class, variable_name, is_local = that_variable

        self.assertEqual(__file__, filepath)
        self.assertEqual(function_or_class.name, "test_findVariablesInDir")

        self.assertTrue(is_local)


if __name__ == "__main__":
    unittest.main()
