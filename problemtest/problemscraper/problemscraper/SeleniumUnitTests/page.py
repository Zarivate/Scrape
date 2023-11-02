from locator import *
from element import BasePageElement

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class SearchTextElement(BasePageElement):
    locator = "q"

class MainPage(BasePage):

    search_text_element = SearchTextElement()

    # Simple check to see whether string is within website/page
    def matches_title(self):
        return "Python" in self.driver.title
    
    def click_go_button(self):
        # Unpack the element that is the GO Button on the Python main page
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()

class SearchResultsPage(BasePage):

    def is_results_found(self):
        return "Nothing found." not in self.driver.page_source