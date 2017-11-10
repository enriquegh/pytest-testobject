import pytest
import appium
import testobject as to


def pytest_addoption(parser):
    group = parser.getgroup('pytest-testobject')
    group.addoption('--to-username',
                    action='store',
                    dest='testobject_username',
                    metavar='TO_USERNAME',
                    help='TestObject username')
    group.addoption('--to-api-key',
                    action='store',
                    dest='testobject_api_key',
                    metavar='TO_API_KEY',
                    help='TestObject project API KEY')
    group.addoption('--to-suite-id',
                action='store',
                dest='testobject_suite_id',
                metavar='TO_SUITE_ID',
                help='TestObject Suite ID that will be used')


def pytest_configure(config):

    testobject_username = None
    testobject_api_key = None
    testobject_suite_id = None

    if not (config.option.help or config.option.showfixtures or config.option.markers):
        if config.getoption('testobject_username'):
            testobject_username = config.getoption('testobject_username')
        if config.getoption('testobject_api_key'):
            testobject_api_key = config.getoption('testobject_api_key')
        if config.getoption('testobject_suite_id'):
            testobject_suite_id = config.getoption('testobject_suite_id')

    assert config.pluginmanager.register(TestObjectPytestPlugin(testobject_username, testobject_api_key, testobject_suite_id),'testobject_helper')

class TestObjectPytestPlugin(object):
    def __init__(self, username, api_key, suite_id):
        self.username = username
        self.api_key = api_key
        self.suite_id = suite_id
        self.devices = self.get_devices()
        self.suite_report = None

    def get_devices(self):
        #TODO:
        # call testobject instance
        # get devices from suite
        # parse response
        return

    @pytest.fixture(scope='class')
    def suite_setup(self, request):
        return


    @pytest.fixture(scope='function')
    def driver_setup(self, request, test_config):
        return

class SuiteReport(object):

    def __init__(self, suite_report_id, test_reports):
        self.suite_report_id = suite_report_id
        self.test_reports = test_reports

    def find_test_report(class_name, method_name, device_id, data_center_id):
        for test_report in test_reports:
            print("wuuuu")
            # compare all of the test reports and find the one that matches all of it
            # if not, throw error

class TestReport(object):

    def __init__(self, class_name, method_name, device_id, data_center_id, test_report_id):

        self.class_name = class_name
        self.method_name = method_name
        self.device_id = device_id
        self.data_center_id = data_center_id
        self.test_report_id = test_report_id


    def get_id():
        return self.test_report_id

    def get_class_name():
        return self.class_name

    def get_method_name():
        return self.method_name

    def get_device_id():
        return self.device_id

    def get_data_center_id():
        return self.data_center_id





