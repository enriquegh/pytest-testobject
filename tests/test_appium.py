import pytest

@pytest.mark.usefixtures("to_suite","to_driver")
class TestAppiumTO(object):

    def test_number_one(to_driver):
        pass

    def test_number_two(to_driver):
        pass

    def test_number_three(to_driver):
        pass