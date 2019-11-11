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
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        @pytest.mark.usefixtures("to_suite","to_driver")
        class TestTODriver(object):

            def test_saucelabs(self, to_driver):

                to_driver.get("https://saucelabs.com")
                expected_title = ("Cross Browser Testing, Selenium "
                                           "Testing, Mobile Testing "
                                           "| Sauce Labs")

                WebDriverWait(to_driver,10).until(EC.title_is(expected_title))
                assert to_driver.title == expected_title

            def test_testobject(self, to_driver):

                to_driver.get("https://app.testobject.com")
                expected_title = ("Sign In | Sauce Labs")

                WebDriverWait(to_driver,10).until(EC.title_is(expected_title))
                assert to_driver.title == expected_title

            @pytest.mark.xfail
            def test_guinea_pig(self, to_driver):

                to_driver.get("https://saucelabs.com/test/guinea-pig")
                id_element = to_driver.find_element_by_id('i_am_an_id')
                assert i_am_an_id != "I am a link"

    """)

    result = testdir.runpytest('--to-username', TO_USERNAME, "--to-api-key",
                               TO_API_KEY, "--to-suite-id", TO_SUITE_ID)

    result.assert_outcomes(passed=4, xfailed=2)
