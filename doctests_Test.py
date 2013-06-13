import unittest
import doctest
import CommentsRemover
import JPChecker

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(CommentsRemover))
    tests.addTests(doctest.DocTestSuite(JPChecker))
    return tests

