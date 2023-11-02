from selenium.webdriver.support.ui import WebDriverWait

# This class represents any other element on the page and will be used to handle it. When any new element is accessed, this class
# will implicitly be used. Will no longer need to implicily wait.
class BasePageElement(object):
    # Set the value for any element on the page 
    def __set__(self, obj, value):
        driver = obj.driver
        # Wait until the lambda is true
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        driver.find_element_by_name(self.locator).clear()
        driver.find_element_by_name(self.locator).send_keys(value)

    # For when the value of an element needs to be accessed
    def __get__(self, obj, owner):
        # Set the webdriver to be equal to the one in use
        driver = obj.driver
        # Wait for element to exist on the page
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_name(self.locator))
        element = driver.find_element_by_name(self.locator)
        # Return the attribute with the corresponding HTML field
        return element.get_attribute("value")
        