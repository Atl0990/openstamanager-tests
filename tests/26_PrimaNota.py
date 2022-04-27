from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from common.RowManager import RowManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class PrimaNota(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Contabilità")

    def test_creazione_primanota(self, modifica = "Prima Nota di Prova (Fatt. n.1 del 01/01/2022)"):
        self.creazione_primanota(causale = "Prima Nota da Modificare")
        self.creazione_primanota(causale = "Prima Nota da Eliminare")

       # Modifica Prima Nota
        self.navigateTo("Prima nota")
        self.wait_loader()

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Causale"]/input')
        element.send_keys('Prima Nota da Modificare')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Causale"]/input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        
        self.input(None,'Causale').setValue(modifica)

        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()


        # Cancellazione Prima nota
        self.navigateTo("Prima nota")
        self.wait_loader()  

        self.find(By.XPATH, '//th[@id="th_Causale"]/i[@class="deleteicon fa fa-times fa-2x"]').click()

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Causale"]/input')
        element.send_keys('Prima Nota da Eliminare')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Causale"]/input'))).send_keys(Keys.ENTER)

        sleep(2)
        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]').click()
        self.wait_loader()
        self.find(By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]').click()
        self.wait_loader()


    def creazione_primanota(self,  causale = str):

        self.navigateTo("Prima nota")
        self.wait_loader() 

        self.find(By.CSS_SELECTOR, '#tabs > li:first-child .btn-primary > .fa-plus').click()
        modal = self.wait_modal()


        self.input(modal, 'Causale').setValue(causale)
        modal = self.wait_modal()

        self.find(By.XPATH, '//span[@id="select2-conto0-container"]').click()
        sleep(1)
        self.find(By.XPATH, '//input[@class="select2-search__field"]').send_keys("100.000010", Keys.ENTER)
        sleep(1)
        self.find(By.XPATH, '//input[@id="avere0"]').send_keys("100,00")


        self.find(By.XPATH, '//span[@id="select2-conto1-container"]').click()
        self.find(By.XPATH, '//input[@class="select2-search__field"]').send_keys("700.000010")
        sleep(1)
        self.find(By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]').click() 
        sleep(1)
        self.find(By.XPATH, '//input[@id="dare1"]').send_keys("100,00")

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()
    

