from selenium.webdriver.support.ui import WebDriverWait

# This class represents any other element on the page and will be used to handle it
class BasePageElement(object):
    def __set__(self, obj, value):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name((self.locator))
        )