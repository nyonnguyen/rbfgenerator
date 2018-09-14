from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import WaitingKeywords
from .elementkeywords import ElementKeywords

__version__ = '1.0.0'


class MyCustomizedLibraryKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.elementkeys = ElementKeywords(ctx)
        self.waiting_management = WaitingKeywords(ctx)

    def get_all_product_in_tab(self, locator):
        return self.find_element(locator).find_elements_by_tag_name("li")

    def click(self, element):
        self.elementkeys.js_click(element)

    @keyword
    def click_on_product_item(self, locator, product_name, product_price):
        """
        :locator: Locator of the tab container
        :product_name: Displayed name of product
        "product_price: Displayed price of product"
        """
        items = self.get_all_product_in_tab(locator)
        for i in items:
            if self.get_product_name(i) == product_name:
                if self.get_product_price(i) == product_price:
                    self.click(self.get_product_clickable_item(i))
                    return
        message = "Item %s - %s not found in %s!" % (product_name, product_price, locator)
        raise AssertionError(message)

    def get_product_url(self, element):
        return self._get_child_element_by_property(element).get_attribute("href").strip()

    def get_product_clickable_item(self, element):
        return self._get_child_element_by_property(element, "url")

    def get_product_name(self, element):
        return self._get_child_element_by_property(element, "name").get_attribute("textContent").strip()

    def get_product_price(self, element):
        return self._get_child_element_by_property(element, "price").get_attribute("textContent").strip().replace("$","")

    def _get_child_element_by_property(self, locator, property):
        return self.find_element(locator).find_element_by_xpath(".//*[@itemprop='"+property+"']")

    @keyword
    def get_alert_div(self):
        return self.driver.find_element_by_xpath("//*[@id='center_column']//*[@class='alert alert-danger']") #get the first element

    @keyword
    def is_alert_visible(self):
        try:
            self.get_alert_div()
            return True
        except:
            return False

    @keyword
    def wait_until_alert_displayed(self, timeout=None, error=None):
        self.waiting_management._wait_until(
          lambda: self.is_alert_visible() == True,
          "Alert was not appeared in <TIMEOUT>",
          timeout,
          error
        )

    @keyword
    def get_login_alert_messages(self):
        alert = self.get_alert_div()
        return [li.get_attribute("textContent").strip for li in alert.find_elements_by_tag_name("li")]

    @keyword
    def is_error_message(self, error_message):
        return error_message in self.get_login_alert_messages()
