# -*- coding: utf-8 -*-
import os


def test_driver_suite_setup(testdir):

    TO_USERNAME = os.environ.get("TO_USERNAME")
    TO_API_KEY = os.environ.get("TO_API_KEY")
    TO_SUITE_ID = os.environ.get("TO_SUITE_ID")

    if not (TO_USERNAME and TO_API_KEY and TO_SUITE_ID):
        # If one of the environment variables is missing fail test
        assert False

    testdir.makepyfile("""
        import pytest

        @pytest.mark.usefixtures("to_suite","to_driver")
        class TestTODriver(object):

            def test_saucelabs(self, to_driver):

                to_driver.get("https://saucelabs.com")
                assert to_driver.title == ("Cross Browser Testing, Selenium "
                                           "Testing, and Mobile Testing "
                                           "| Sauce Labs")

            def test_testobject(self, to_driver):

                to_driver.get("https://testobject.com")
                assert to_driver.title == ("TestObject – Android and iOS "
                                           "Mobile App Testing Made Easy")


    """)

    testdir.runpytest('--to-username', TO_USERNAME, "--to-api-key", TO_API_KEY,
                      "--to-suite-id", TO_SUITE_ID)
