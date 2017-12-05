# -*- coding: utf-8 -*-

import pytest
from _pytest.main import EXIT_INTERRUPTED


@pytest.mark.smoke
@pytest.mark.parametrize("flags",
                         ["--to-username",
                          "--to-api-key",
                          "--to-suite-id"
                          ]
                         )
def test_required_flag_output(testdir, flags):
    ''' Verifies required flags fail if no input is given '''

    result = testdir.runpytest(flags)

    assert result.ret == EXIT_INTERRUPTED

    result.stderr.fnmatch_lines([
        '*error: argument {}: expected one argument'.format(flags)
    ])


@pytest.mark.smoke
def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'testobject:',
        '*--to-username=TO_USERNAME',
        '*TestObject username',
        '*--to-api-key=TO_API_KEY',
        '*TestObject project API KEY',
        '*--to-suite-id=TO_SUITE_ID',
        '*TestObject Suite ID that will be used'

    ])
