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


class FasceOrarie(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Attività")

    def test_creazione_fasce_orarie(self):
        # Creazione fasce orarie *Required*
        self.creazione_fasce_orarie("Fascia Oraria di Prova da Modificare", "8:00", "10:00")
        self.creazione_fasce_orarie("Fascia Oraria di Prova da Eliminare", "8:00", "10:00")

        # Modifica fasce orarie
        self.modifica_fasce_orarie("Fascia Oraria di Prova")

        # Cancellazione fasce orarie
        self.elimina_fasce_orarie()


    def creazione_fasce_orarie(self, nome = str, inizio=str, fine=str):
        self.navigateTo("Fasce orarie")
        self.wait_loader()  

        self.find(By.CSS_SELECTOR, '#tabs > li:first-child .btn-primary > .fa-plus').click()
        modal = self.wait_modal()

        self.input(None,'Ora inizio').setValue(inizio)
        self.input(None,'Ora fine').setValue(fine)
        self.input(modal, 'Nome').setValue(nome)

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_fasce_orarie(self, modifica:str):
        self.navigateTo("Fasce orarie")
        self.wait_loader()

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Nome"]/input')
        element.send_keys('Fascia Oraria di Prova da Modificare')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        
        self.input(None,'Nome').setValue(modifica)

        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()

        self.navigateTo("Fasce orarie")
        self.wait_loader()  

        self.find(By.XPATH, '//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times fa-2x"]').click()

    def elimina_fasce_orarie(self):
        self.navigateTo("Fasce orarie")
        self.wait_loader()  

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Nome"]/input')
        element.send_keys('Fascia Oraria di Prova da Eliminare')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys(Keys.ENTER)

        sleep(2)
        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]').click()
        self.wait_loader()
        self.find(By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]').click()
        self.wait_loader()