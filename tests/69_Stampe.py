from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Stampe(Test):
    def setUp(self):
        super().setUp()
        self.expandSidebar("Strumenti")


    def test_stampe(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Stampe")
        self.wait_loader()