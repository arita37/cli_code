#!/usr/bin/env python3

import unittest

from src import ast_analyzer


class TestFileFinder(unittest.TestCase):
    def test_corner_cases(self):
        with self.assertRaises(SyntaxError):
            ast_analyzer.analyzeSource("Lorem ipsum dolor sit amet.")

    def test_file_finder(self):
        variables = ast_analyzer.analyzeSource(
            """
#!/usr/bin/env python3


def hello(msg="Hello world!"):
  print(msg)


if __name__ == "__main__":
  hello()
"""
        )

        want = [
            ("(global)", "__name__", False),
            ("(global)", "hello", False),
            ("hello", "msg", True),
            ("hello", "print", False),
        ]

        got = sorted(
            (
                function_or_class.name if function_or_class is not None else "(global)",
                variable_name,
                is_local,
            )
            for ((function_or_class, variable_name), is_local) in variables.items()
        )

        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
