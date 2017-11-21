import pytest
import appium
import testobject as to

import logging
import logging.config
import yaml

logging.config.dictConfig(yaml.load(open('logconf.yaml', 'r')))

log = logging.getLogger(__name__)

class TestObjectError(Exception):
    pass

class TestObjectCredentialError(Exception):
    pass


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
            log.debug("Grabbing {} from flag. Result: {}".format("testobject_username",testobject_username))

        if config.getoption('testobject_api_key'):
            testobject_api_key = config.getoption('testobject_api_key')
            log.debug("Grabbing {} from flag. Result: {}".format("testobject_api_key",testobject_api_key))
            

        if config.getoption('testobject_suite_id'):
            testobject_suite_id = config.getoption('testobject_suite_id')
            log.debug("Grabbing {} from flag. Result: {}".format("testobject_suite_id",testobject_suite_id))

        if not (testobject_username and testobject_api_key and testobject_suite_id):
            raise TestObjectCredentialError

        assert config.pluginmanager.register(TestObjectPytestPlugin(testobject_username, testobject_api_key, testobject_suite_id),'testobject_helper')

class TestObjectPytestPlugin(object):
    def __init__(self, username, api_key, suite_id):
        self.username = username
        self.api_key = api_key
        self.suite_id = suite_id
        self.devices = self.get_devices()
        self.suite_report = None

    def get_devices(self):

        testobject = to.TestObject(self.username, self.api_key)

        response = testobject.suites.get_devices_ids(self.suite_id)

        if response.ok:
            devices = []
            datacenter_ids = response.json()
            for datacenter in datacenter_ids:
                for device_descriptor in datacenter['deviceDescriptorIds']:
                    device_descriptors = {}
                    device_descriptors['dataCenterId'] = datacenter['dataCenterId']
                    device_descriptors['deviceId'] = device_descriptor
                    devices.append(device_descriptors)
            log.debug("FORMATTED DEVICES ARE:")
            log.debug(devices)
            
            return devices
        else:
            raise TestObjectError

    def pytest_generate_tests(self, metafunc):
        #Parametrize test and create test_config
        log.debug(metafunc.fixturenames)
        if "to_driver" in metafunc.fixturenames:
            metafunc.parametrize("test_config", self.devices, scope="function")


    @pytest.fixture(scope='class')
    def to_suite(self, request):

        class_name = request.node.name
        log.debug("Class name is: {}".format(class_name))
        test_names = set() # To avoid grabbing test names multiple times

        for item in request.session.items:
            if item.originalname not in test_names:
                test_names.add(item.originalname)
        log.debug("Test names are: {}".format(test_names))

        suite_request = []
        for test in test_names:
            test_request = {}
            test_request["className"] = class_name
            test_request["methodName"] = test
            for device in self.devices:
                temp_request = {} # temporary dict to add two other dicts
                temp_request.update(test_request)
                temp_request.update(device)
                suite_request.append(temp_request)
        log.debug("Suite request is: {}".format(suite_request))

        to_instance = to.TestObject(self.username, self.api_key)

        suite = to_instance.suites.start_suite(self.suite_id, suite_request)

        if suite.ok:
            log.debug("Suite returned successfully")
            test_list = []
            response = suite.json()
            suite_report_id = response['id']
            for test in response['testReports']:
                
                test_id = test['id']
                class_name = test['test']['className']
                method_name = test['test']['methodName']
                device_id = test['test']['deviceId']
                data_center_id = test['test']['dataCenterId']
                
                test_report = TestReport(class_name, method_name, device_id, data_center_id, test_id)
                test_list.append(test_report)

            self.suite_report = SuiteReport(suite_report_id, test_list)

        else:
            raise TestObjectError(suite.reason, suite.request.body)
        
        yield self.suite_report


    @pytest.fixture(scope='function')
    def to_driver(self, request, test_config):

        desired_caps = {}
        url = None

        class_name = request.cls.__name__
        method_name = request.node.originalname
        device_id = test_config['deviceId']
        data_center_id = test_config['dataCenterId']

        test_report = self.suite_report.find_test_report(class_name, method_name, device_id, data_center_id)


        if data_center_id is 'US':
            url = 'https://us1.appium.testobject.com/wd/hub'
        else:
            url = 'https://eu1.appium.testobject.com/wd/hub'

        if test_report:
            test_report_id = test_report.get_id()

            desired_caps['testobject_api_key'] = self.api_key
            desired_caps['testobject_device'] = device_id
            desired_caps['testobject_test_report_id'] = test_report_id

            request.instance.driver = appium.webdriver.Remote(url, desired_caps)

        #ADD FINALIZER INSTEAD OF YIELD
            def teardown():
                request.instance.driver.quit()
                request.addfinalizer(teardown)


        # Grab test config
        # Grab suite_report and call find_test_report
        # Start remote web driver and yield it

class SuiteReport(object):

    def __init__(self, suite_report_id, test_reports):
        self.suite_report_id = suite_report_id
        self.test_reports = test_reports

    def find_test_report(self, class_name, method_name, device_id, data_center_id):
        for test_report in self.test_reports:
            test_class_name = test_report.get_class_name()
            test_method_name = test_report.get_method_name()
            test_device_id = test_report.get_device_id()
            test_data_center_id = test_report.get_data_center_id()

            if test_class_name is class_name and test_method_name is method_name and test_device_id is device_id and test_data_center_id is data_center_id:
                log.debug("Match found {}", test_report)
                return test_report

        return None

class TestReport(object):

    def __init__(self, class_name, method_name, device_id, data_center_id, test_report_id):

        self.class_name = class_name
        self.method_name = method_name
        self.device_id = device_id
        self.data_center_id = data_center_id
        self.test_report_id = test_report_id


    def get_id(self):
        return self.test_report_id

    def get_class_name(self):
        return self.class_name

    def get_method_name(self):
        return self.method_name

    def get_device_id(self):
        return self.device_id

    def get_data_center_id(self):
        return self.data_center_id





