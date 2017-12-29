#User Guide

##Quick Start
The pytest-testobject plugin consists of two fixtures `to_suite` and `to_driver` and are meant to be used inside a class.

A simple use of these would look like this:

```python

@pytest.mark.usefixtures("to_suite","to_driver")
class TestTODriver(object):

    def test_saucelabs(self, to_driver):
        #Do stuff like to_driver.get(...)

```

Once you have your test that uses both fixtures you need to pass in your TestObject username, project api key, and suite ID as flags.

```bash
$ pytest --to-username USERNAME --to-api-key API_KEY --to-suite-id SUITE_ID
```

##to_suite fixture

This fixture is in charge of grabbing the suite ID, collecting the devices stated on the suite and creating a test for each of them (e.g. two devices with two tests would created four tests total).
It also saves the suite report id as well as the test report id to make sure we can link all tests appropriately and they show up correctly in the Suite Report UI on TestObject.

This fixture is very hands off and only needs to be declared at the top of the class. There's nothing that needs to be done once used.

##to_driver fixture

The to_driver fixture does some logic to route the test to the correct device like adding the test_report_id and the necessary desired_capabilities.
This fixture does need to be included in every test and will act as the main driver that is used to perform actions on devices.

For the moment, it's not possible to add more desired_capabilities to the driver.


##Notes

For more information on the Appium API you can go look [here](https://appium.readthedocs.io/en/stable/README/).
For more information on the TestObject API you can go look [here](https://github.com/enriquegh/testobject-python-api)
