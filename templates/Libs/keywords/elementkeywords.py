from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import ElementKeywords as SeleniumElementKeywords
from selenium.webdriver.common.keys import Keys
import os


class ElementKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.element_management = SeleniumElementKeywords(ctx)

    @keyword
    def clear_textfield_value(self, locator):
        text = self.element_management.get_value(locator)
        i = 0
        while i < len(text):
            i += 1
            self.element_management.press_key(locator, Keys.BACK_SPACE)
            self.element_management.press_key(locator, Keys.DELETE)

    @keyword
    def scroll_to_element(self, locator):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))

    def _scroll_to_left_of_webElement(self, element):
        self.driver.execute_script("arguments[0].scrollTo(0,0);", element)

    @keyword
    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @keyword
    def get_child_element_by_tag_and_attribute(self, element, tag, attribute_name, attribute_value):
        child_elements = element.find_elements_by_tag_name(tag)
        for child in child_elements:
            if child.get_attribute(attribute_name).strip() == attribute_value:
                return child
        message = "Child element '%s = %s' not found!" % (attribute_name, attribute_value)
        raise AssertionError(message)
