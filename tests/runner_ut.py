#!/usr/bin/env python

import sys
import unittest

try:
    import runner.runner as runner
except ImportError as imperr:
    print "ImportError: %s \nResolve by adding path to PYTHONPATH" % (imperr)
    sys.exit()


class RUNNERTest(unittest.TestCase):
    '''
    Collection of test cases for the ucsutils module.
    '''
    def test_runner_basic(self):
        '''
        basic runner test
        '''
        runobj = runner.Runner()


if __name__ == '__main__':
    unittest.main()

