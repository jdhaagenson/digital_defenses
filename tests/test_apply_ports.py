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

        
    def test_empty_include(self):
        """
        Checks for handling empty include_ports input
        """
        apply_port_exclusions = apply_ports.apply_port_exclusions
        test = apply_port_exclusions([], [[8080, 8080]])
        self.assertEqual([], test)


if __name__ == '__main__':
    unittest.main()

