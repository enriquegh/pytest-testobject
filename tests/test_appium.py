import pytest

@pytest.mark.usefixtures("to_suite","to_driver")
class TestAppiumTO(object):

    def test_number_one(self, to_driver):
        print('Going to Sauce Labs')
        to_driver.get("https://saucelabs.com")
        # to_driver.quit()
        

    def test_number_two(self, to_driver):
        print('Going to TestObject')
        to_driver.get("https://testobject.com")
        