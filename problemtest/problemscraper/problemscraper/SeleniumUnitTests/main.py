import unittest
from selenium import webdriver
import page
from problemscraper.settings import DRIVER_PATH, BRAVE_PATH

class PythonSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.driver.get("http://www.python.org")


    def test_example(self):
        print("Test")
        assert True

    def tearDown(self):
        self.driver.close()


if __name__ == "main":
    unittest.main()