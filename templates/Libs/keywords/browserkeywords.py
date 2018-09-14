from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox

from SeleniumLibrary.keywords import WaitingKeywords

import os
from ..utilities import Utilities

__version__ = '1.0.0'


class BrowserKeywords(LibraryComponent):

    FIREFOX_DRIVER_PATH = "/Webdrivers/firefox/firefox"
    CHROME_DRIVER_PATH = "\Webdrivers\chromedriver\chromedriver"

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.waiting_management = WaitingKeywords(ctx)
        self.browser_management = BrowserManagementKeywords(ctx)

    @keyword
    def setup_browser_driver(self, browser, path=''):
        """
        Create instance of selenium webdriver base on driver type
        :browser: browser type: chrome | firefox | ie
        :path: the path of executable driver
        """
        browser = browser.strip().lower()
        if browser == 'firefox':
            if path == '':
                path = self.get_project_path() + self.FIREFOX_DRIVER_PATH
            driver = Firefox(executable_path=self.format_executable_path(path))
        else:
            if path == '':
                path = self.get_project_path() + self.CHROME_DRIVER_PATH
            driver = Chrome(self.format_executable_path(path))
        return self.browser_management.ctx.register_driver(driver, None)

    def format_executable_path(self, path):
        if ".exe" in path:
            return path
        else:
            return path if os.sep == '/' else path + ".exe"

    def get_project_path(self):
        """
        Get the root directory of the project
        """
        return os.path.dirname(__file__).replace("LIBRARY_PATH_TO_DEFINE",'')

    def get_location(self):
        return self.browser_management.get_location()

    @keyword
    def wait_until_location_is(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
          lambda: self.get_location() == expected,
          "Location was not match '%s' in <TIMEOUT>. Actual value was '%s'" % (expected, self.get_location()),
          timeout,
          error
        )

    @keyword
    def wait_until_location_is_not(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: self.get_location() != expected,
            "Location did not change to value different to '%s' in <TIMEOUT>" % (expected, self.get_location()),
            timeout,
            error
        )

    @keyword
    def wait_until_location_contains(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected in self.get_location(),
            "Location '%s' did not contain '%s' in <TIMEOUT>" % (self.get_location(), expected),
            timeout,
            error
        )

    @keyword
    def location_should_not_be(self, expected):
        actual = self.get_location()
        if expected == actual:
            message = "Location should not be '%s' but it was NOT" % (expected)
            raise AssertionError(message)

    @keyword
    def element_css_property_value_should_be(self, locator, property_name, expected, message=''):
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if expected != actual:
            if not message:
                message = "The css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def element_color_css_property_value_should_be(self, locator, property_name, expected, message=''):
        if self._is_rgb_color(expected):
            expected = self._convert_rgb_to_hex(expected)
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if self._is_rgb_color(actual):
            actual = self._convert_rgb_to_hex(actual)
        if expected != actual:
            if not message:
                message = "The color related css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def wait_until_element_css_property_value_is(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self.find_element(locator).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not match '%s' in <TIMEOUT>. Actual value is '%s'"
            % (property_name, locator, expected, self.find_element(locator).value_of_css_property(property_name)),
            timeout,
            error
        )

    @keyword
    def wait_until_element_css_property_value_is_not(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self.find_element(locator).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def wait_until_element_color_css_property_value_is(self, locator, property_name, expected, timeout=None,
                                                       error=None):
        if Utilities()._is_rgb_color(expected):
            expected = Utilities()._convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self.find_element(locator)
            actual = element.value_of_css_property(property_name)
            if Utilities()._is_rgb_color(actual):
                actual = Utilities()._convert_rgb_to_hex(actual)
            return actual == expected

        self.waiting_management._wait_until(
            lambda: check_css_property_value,
            "The color related css value '%s' of element '%s' did not match '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def wait_until_element_color_css_property_value_is_not(
            self, locator, property_name, expected, timeout=None, error=None):
        if self._is_rgb_color(expected):
            expected = Utilities()._convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self.find_element(locator)
            actual = element.value_of_css_property(property_name)
            if Utilities()._is_rgb_color(actual):
                actual = Utilities()._convert_rgb_to_hex(actual)
            return actual == expected

        self.waiting_management._wait_until(
            lambda: check_css_property_value,
            "The color related css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )
