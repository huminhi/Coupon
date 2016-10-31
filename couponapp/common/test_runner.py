'''
Created on May 7, 2010

@author: KhoaTran
'''
import unittest
from django.conf import settings
from django.db.models import get_app, get_apps
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.testcases import OutputChecker, TestCase
from django.test.simple import build_suite, build_test, reorder_suite

# The module name for tests outside models.py
TEST_MODULE = 'tests'

doctestOutputChecker = OutputChecker()

def create_test_db(connection, verbosity=1):
    """
    Creates a test database, prompting the user for confirmation if the
    database already exists. Returns the name of the test database created.
    """
    if verbosity >= 1:
        print "Connecting database..."

    connection.close()
    test_database_name = settings.DATABASE_NAME 
    connection.settings_dict["DATABASE_NAME"] = test_database_name
    connection.settings_dict["DATABASE_SUPPORTS_TRANSACTIONS"] = settings.DATABASE_SUPPORTS_TRANSACTIONS

    # Get a cursor (even though we don't need one yet). This has
    # the side effect of initializing the test database.
    cursor = connection.cursor()

    return test_database_name
    
def destroy_test_db(connection, verbosity=1):
    """
    Destroy a test database, prompting the user for confirmation if the
    database already exists. Returns the name of the test database created.
    """
    if verbosity >= 1:
        print "Closing database..."
    connection.close()

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    """
    Run the unit tests for all the test labels in the provided list.
    Labels must be of the form:
     - app.TestClass.test_method
        Run a single specific test method
     - app.TestClass
        Run all the test methods in a given class
     - app
        Search for doctests and unittests in the named application.

    When looking for tests, the test runner will look in the models and
    tests modules for the application.

    A list of 'extra' tests may also be provided; these tests
    will be added to the test suite.

    Returns the number of tests that failed.
    """
    setup_test_environment()

    settings.DEBUG = False
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))
    else:
        for app in get_apps():
            suite.addTest(build_suite(app))

    for test in extra_tests:
        suite.addTest(test)

    suite = reorder_suite(suite, (TestCase,))

    from django.db import connection

    create_test_db(connection, verbosity)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    destroy_test_db(connection, verbosity)

    teardown_test_environment()

    return len(result.failures) + len(result.errors)