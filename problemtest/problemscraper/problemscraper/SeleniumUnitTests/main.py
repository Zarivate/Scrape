import unittest
from selenium import webdriver
import page

class PythonSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("C:\\Program Files\\chromedriver.exe")
        self.driver.get("http://www.python.org")


    def test_example(self):
        print("Test")
        assert True

    # Test to check whether title matches
    def test_title(self):
        mainPage = page.MainPage()
        assert mainPage.matches_title()

    def tearDown(self):
        self.driver.close()


if __name__ == "main":
    unittest.main()