import unittest
from selenium import webdriver
import page

class PythonSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("C:\\Program Files\\chromedriver.exe")
        self.driver.get("http://www.python.org")

    # Test to check whether title matches
    def test_search_python(self):
        mainPage = page.MainPage(self.driver),
        assert mainPage.matches_title()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_results_page = page.SearchResultsPage(self.driver)
        assert search_results_page.is_results_found()

    def tearDown(self):
        self.driver.close()


if __name__ == "main":
    unittest.main()