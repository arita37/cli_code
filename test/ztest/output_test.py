#!/usr/bin/env python3

import io
import unittest
import unittest.mock

from src import output


class TestOutput(unittest.TestCase):
    HEADER_ROW = "filepath,function_or_class_name,variable_name,is_local\n"

    def test_corner_cases(self):
        mock_file_handle = io.StringIO()
        output.writeCSV(set(), mock_file_handle)

        got = mock_file_handle.getvalue()
        self.assertEqual(TestOutput.HEADER_ROW, got)

    def test_output(self):
        mock_file_handle = io.StringIO()
        mock_function_or_class = unittest.mock.Mock()
        mock_function_or_class.name = "function_name"

        output.writeCSV(
            {
                ("source.py", mock_function_or_class, "global_variable", False),
                ("source.py", mock_function_or_class, "local_variable", True),
            },
            mock_file_handle,
        )

        want = TestOutput.HEADER_ROW
        want += "source.py,function_name,global_variable,False\n"
        want += "source.py,function_name,local_variable,True\n"
        got = mock_file_handle.getvalue()
        self.assertEqual(sorted(want), sorted(got))


if __name__ == "__main__":
    unittest.main()
