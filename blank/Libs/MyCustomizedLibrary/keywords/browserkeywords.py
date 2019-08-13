from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.ie.options import Options as IeOptions

from SeleniumLibrary.keywords import WaitingKeywords

import os
import shutil
import xlrd
import csv
import socket
import re
from os import walk
from ..utilities import Utilities

__version__ = '1.0.1'

_BROWSER_TYPE_KEY = "TYPE"
_BROWSER_BINARY_PATH_KEY = "BROWSER_BINARY_PATH"
_BROWSER_DRIVER_PATH_KEY = "BROWSER_DRIVER_PATH"
_BROWSER_HEADLESS_MODE = "HEADLESS"
_BROWSER_WINDOW_SIZE = "WINDOW_SIZE"
_BROWSER_ARGUMENTS_KEY = "BROWSER_ARGUMENTS"

_DEFAULT_DOWNLOAD_PATH = "Downloads"

_DEFAULT_LIBRARY_PATH = '<relative_path_to_here>'

_XLSX_EXTENSION = '.xlsx'
_CSV_EXTENSION = '.csv'


def format_os_path(path):
    return path.replace('\\', '/') if os.sep == '/' else path.replace('/', '\\')


def format_executable_path(path):
    if os.name == 'nt':
        path = path if ".exe" in path else path + ".exe"
    return format_os_path(path)


def get_project_path():
    """
    Get the root directory of the project
    """
    # return os.path.dirname(__file__).replace(_DEFAULT_LIBRARY_PATH, '')
    return os.getcwd()


def get_download_path(re_path=''):
    d_path = get_project_path() + '\\' + (_DEFAULT_DOWNLOAD_PATH if re_path == '' else re_path)
    return format_os_path(d_path)


def enable_download_in_headless_chrome(driver, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    # Source: StackOverflow
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.waiting_management = WaitingKeywords(ctx)
        self.browser_management = BrowserManagementKeywords(ctx)

    @keyword
    def setup_browser_driver(self, settings):
        """
        Create instance of selenium webdriver base on driver type
        :settings: dictionary of browser setting. Sample:
        BROWSER:
          TYPE: chrome
          BROWSER_BINARY_PATH: <path_name_of_browser_binary>
          BROWSER_DRIVER_PATH: <path_name_of_browser_driver>
          HEADLESS: True
          WINDOW_SIZE: 1920,1080
          BROWSER_ARGUMENTS:
            no-sandbox
            arg2=value2
        """
        # init browsers
        firefox = AosBrowser('firefox', 'ff', None, '/Webdrivers/firefoxdriver/geckodriver', False, None, None)
        chrome = AosBrowser('chrome', 'gc', None, '/Webdrivers/chromedriver/chromedriver', False, None, None)
        ie = AosBrowser('ie', 'ie', None, '/Webdrivers/iedriver/IEDriverServer', False, None, None)
        _BROWSER_MAP = {'firefox': firefox,
                        'chrome': chrome,
                        'ie': ie}

        browser_type = settings.get(_BROWSER_TYPE_KEY).strip().lower()
        bin_path = settings.get(_BROWSER_BINARY_PATH_KEY, None)
        driver_path = settings.get(_BROWSER_DRIVER_PATH_KEY)
        headless_mode = settings.get(_BROWSER_HEADLESS_MODE, False)
        window_size = settings.get(_BROWSER_WINDOW_SIZE, None)
        browser_args = settings.get(_BROWSER_ARGUMENTS_KEY, None)

        detected_browser = _BROWSER_MAP[browser_type]
        detected_browser.set_bin_path(bin_path)
        detected_browser.set_driver_path(driver_path)
        detected_browser.set_headless(headless_mode)
        detected_browser.set_window_size(window_size)
        detected_browser.set_args(browser_args)

        driver = detected_browser.get_driver()
        driver.delete_all_cookies()
        if detected_browser.is_maximum():
            driver.maximize_window()
        return self.browser_management.ctx.register_driver(driver, None)

    def get_location(self):
        return self.browser_management.get_location()

    @keyword
    def wait_until_location_is(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: self.get_location() == expected,
            "Location was not match '%s' in <TIMEOUT>. Actual value was '%s'" %
            (expected, self.get_location()),
            timeout,
            error
        )

    @keyword
    def wait_until_location_is_not(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: self.get_location() != expected,
            "Location did not change to value different to '%s' in <TIMEOUT>. Actual value was '%s'" %
            (expected, self.get_location()),
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
            message = "Location should not be '%s' but it was NOT" % expected
            raise AssertionError(message)

    @keyword
    def element_css_property_value_should_be(self, locator, property_name, expected, message=''):
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if expected != actual:
            if not message:
                message = "The css value '%s' of element '%s' should have been '%s' but " \
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def element_color_css_property_value_should_be(self, locator, property_name, expected, message=''):
        if Utilities.is_rgb_color(expected):
            expected = Utilities.convert_rgb_to_hex(expected)
        element = self.find_element(locator)
        actual = element.value_of_css_property(property_name)
        if Utilities.is_rgb_color(actual):
            actual = Utilities.convert_rgb_to_hex(actual)
        if expected.upper() != actual.upper():
            if not message:
                message = "The color related css value '%s' of element '%s' should have been '%s' but " \
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
        if Utilities.is_rgb_color(expected):
            expected = Utilities.convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self.find_element(locator)
            actual = element.value_of_css_property(property_name)
            if Utilities.is_rgb_color(actual):
                actual = Utilities.convert_rgb_to_hex(actual)
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
        if Utilities.is_rgb_color(expected):
            expected = Utilities.convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self.find_element(locator)
            actual = element.value_of_css_property(property_name)
            if Utilities.is_rgb_color(actual):
                actual = Utilities.convert_rgb_to_hex(actual)
            return actual == expected

        self.waiting_management._wait_until(
            lambda: check_css_property_value,
            "The color related css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def cleanup_download(self):
        shutil.rmtree(get_download_path(), ignore_errors=True)

    @keyword
    def get_single_downloaded_file(self, ext):
        for root, dirs, files in walk(get_download_path()):
            for f in files:
                if f.endswith(ext):
                    return os.path.join(root, f)
        raise AssertionError("No match downloaded file")

    @keyword
    def wait_until_file_downloaded(self, file_name='', ext='', timeout=30, error=None):
        self.waiting_management._wait_until(
            lambda: Utilities().is_downloaded_file_has_extension(get_download_path(file_name), ext),
            "There is no download file in <TIMEOUT>.",
            timeout,
            error
        )

    def _get_actual_downloaded_file(self, extension, file_name=''):
        self.wait_until_file_downloaded(file_name, extension)
        return file_name if file_name else self.get_single_downloaded_file(extension)

    @keyword
    def get_downloaded_xlsx_data(self, file_name=''):
        file_name = self._get_actual_downloaded_file(_XLSX_EXTENSION, file_name)
        data = []
        try:
            wb = xlrd.open_workbook(file_name)
        except:
            raise AssertionError("Failed to open XLSX downloaded file!")
        ws = wb.sheet_by_index(0)
        for row in ws.get_rows():
            for cell in row:
                data.append(cell.value)
        return data

    @keyword
    def get_downloaded_csv_data(self, file_name=''):
        file_name = self._get_actual_downloaded_file(_CSV_EXTENSION, file_name)
        data = []
        try:
            with open(file_name, encoding='utf-8-sig') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    for item in row:
                        data.append(item.strip())
                return data
        except:
            raise AssertionError("Failed to open CSV downloaded file!")

    @keyword
    def current_remote_ip_address(self):
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    @keyword
    def current_router_ip_address(self, aos_url):
        temp = aos_url.replace("http://", "")
        if temp.find(":") > -1:
            router_address = temp.split(":")[0]
        elif temp.find("/") > -1:
            router_address = temp.split("/")[0]
        else:
            router_address = temp
        return router_address


class AosBrowser(object):

    def __init__(self, b_type, short_type, bin_path, driver_path, headless, window_size, args):
        self.b_type = b_type
        self.short_type = short_type
        self.bin_path = bin_path
        self.driver_path = driver_path
        self.headless = headless
        self.window_size = window_size
        self.args = args

    def set_type(self, b_type):
        self.b_type = b_type

    def get_type(self):
        return self.b_type

    def set_short_type(self, short_type):
        self.short_type = short_type

    def get_short_type(self):
        return self.short_type

    def set_bin_path(self, bin_path):
        self.bin_path = bin_path

    def get_bin_path(self):
        return self.bin_path

    def set_driver_path(self, driver_path):
        if driver_path is not None:
            self.driver_path = driver_path
        else:
            self.driver_path = format_executable_path(get_project_path() + self.driver_path)

    def get_driver_path(self):
        return self.driver_path

    def set_headless(self, headless):
        self.headless = headless

    def get_headless(self):
        return self.headless

    def set_window_size(self, window_size):
        self.window_size = window_size

    def get_window_size(self):
        return self.window_size

    def set_args(self, args):
        self.args = args

    def get_args(self):
        return self.args

    def get_options(self):
        if self.get_type() == 'firefox':
            options = FirefoxOptions()
            if self.get_args():
                for arg in self.get_args().split():
                    options.add_argument('--' + arg)
            if self.bin_path:
                options.binary_location(self.bin_path)
            if self.get_headless():
                options.headless = True
            if self.get_window_size():
                win_size = self.get_window_size().split(',')
                options.add_argument('--width=' + win_size[0])
                options.add_argument('--height=' + win_size[1])
            # Set download path
            options.set_preference('browser.download.folderList', 2)
            options.set_preference('browser.download.dir', get_download_path())
            options.set_preference('browser.download.manager.showWhenStarting', False)
            options.set_preference('browser.helperApps.alwaysAsk.force', False)
            options.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/octet-stream")
            # options.set_preference('browser.helperApps.neverAsk.openFile', "application/octet-stream")
        elif self.get_type() == 'ie':
            options = IeOptions()
            options.ignore_protected_mode_settings = False
            options.require_window_focus = True
            options.native_events = False
            # proceed IE options here
        else:
            options = ChromeOptions()
            if self.get_args():
                for arg in self.get_args().split():
                    options.add_argument(arg)
            if self.bin_path:
                options.binary_location(self.bin_path)
            if self.get_headless():
                options.headless = True
            if self.get_window_size():
                options.add_argument('--window-size=' + self.get_window_size())
            # Set download path
            prefs = {}
            prefs["download.prompt_for_download"] = 0
            prefs["download.default_directory"] = get_download_path()
            options.add_experimental_option("prefs", prefs)
        return options

    def get_driver(self):
        if self.get_type() == 'firefox':
            driver = Firefox(firefox_profile=None, firefox_binary=self.bin_path,
                             timeout=30, capabilities=None, proxy=None,
                             executable_path=self.get_driver_path(), options=self.get_options())
        elif self.get_type() == 'ie':
            driver = Ie(executable_path=self.driver_path, options=self.get_options())
            if self.get_window_size():
                driver.set_window_size(self.get_window_size())
        else:
            print(self.get_driver_path())
            driver = Chrome(executable_path=self.get_driver_path(), options=self.get_options())
            # This work-around to enable download mode in headless chrome
            # https://bugs.chromium.org/p/chromium/issues/detail?id=696481
            # TODO: Check if the latest chromedriver update or not
            enable_download_in_headless_chrome(driver, get_download_path())
        return driver

    def is_maximum(self):
        return self.get_window_size() is None
