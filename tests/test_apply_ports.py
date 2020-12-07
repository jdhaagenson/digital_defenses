"""
Unit test cases for apply_ports.py
"""

__author__ = 'Jordan Haagenson'

import importlib
import inspect
import sys
import unittest
from io import StringIO

import apply_ports

# suppress __pycache__ and .pyc files
sys.dont_write_bytecode = True

PKG_NAME = 'apply_ports'

class Capturing(list):
    """Context manager for capturing stdout from function call"""

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio # free up some memory
        sys.stdout = self._stdout

class TestApplyPorts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        # check for python3
        cls.assertGreaterEqual(cls, sys.version_info[0], 3)
        # This will import the module to be tested
        cls.module = importlib.import_module(PKG_NAME)
        # make a dictionary of each function in the test module
        cls.funcs = {
            k: v for k, v in inspect.getmembers(
                cls.module, inspect.isfunction
            )
        }
        # check the funcs for required functions
        assert "apply_port_exclusions" in cls.funcs, "Missing the required 'apply_port_exclusions()' function"

    def setUp(self):
        self.include = [[30, 45], [800, 899], [8000, 9000]]
        self.exclude = [[22, 22], [45, 47], [8080, 8080], [843, 855]]
        self.correct_output = [[30, 44], [800, 842], [856, 899], [8000, 8079], [8081, 9000]]


    def test_apply_port_exclusions(self):
        """
        Test whether output conforms to code examples given
        """
        apply_port_exclusions = apply_ports.apply_port_exclusions
        test = apply_port_exclusions([[1, 65535]], [[1000, 2000], [500, 2500]])
        self.assertListEqual([[1, 499], [2501, 65535]], test)

    def test_callable(self):
        self.assertTrue(
            callable(apply_ports.apply_port_exclusions),
            msg="The apply_port_exclusions function is missing"
        )

    def test_order(self):
        """Out of order inputs should not have different outputs"""
        apply_port_exclusions = apply_ports.apply_port_exclusions
        solution = [[22, 23], [80, 80], [8000, 8079], [8081, 9000]]
        out_of_order = apply_port_exclusions([[80, 80], [22, 23], [8000, 9000]],
                                         [[1024, 1024], [8080, 8080]])
        self.assertListEqual(out_of_order, solution, f"Expected {solution}, got {out_of_order}")
        in_order = apply_port_exclusions([[8000, 9000], [80, 80], [22, 23]],
                                             [[1024, 1024], [8080, 8080]])
        self.assertListEqual(in_order, out_of_order, f"Expected {in_order} == {out_of_order}. "
                                                 f"You are getting different output with different order of same params"
                         )

    def test_empty_include(self):
        """
        Checks for handling empty include_ports input
        """
        apply_port_exclusions = apply_ports.apply_port_exclusions
        test = apply_port_exclusions([], [[8080, 8080]])
        self.assertEqual([], test)


if __name__ == '__main__':
    unittest.main()

