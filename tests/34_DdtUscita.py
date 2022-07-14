from common.Test import Test, get_html
from common.RowManager import RowManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DdtUscita(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Magazzino")


    def test_creazione_ddt_uscita(self):
        # Crea un nuovo ddt al cliente "Cliente". *Required*
        importi = RowManager.list()
        self.creazione_ddt_uscita("Cliente", "2", importi[0])
        self.creazione_ddt_uscita("Cliente", "3", importi[0])

        # Modifica Ddt
        self.modifica_ddt("Ddt di Prova Modificato")
        
        # Cancellazione Ddt
        self.elimina_ddt()


    def creazione_ddt_uscita(self, cliente: str, causale: str, file_importi: str):
        self.navigateTo("Ddt in uscita")

        # Crea un nuovo ddt al cliente indicato. 
        # Apre la schermata di nuovo elemento
        self.find(By.CSS_SELECTOR, '#tabs > li:first-child .btn-primary > .fa-plus').click()
        modal = self.wait_modal()

        select = self.input(modal, 'Destinatario')
        select.setByText(cliente)

        select = self.input(modal, 'Causale trasporto')
        select.setByIndex(causale)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        #toast = self.driver.find_elements(By.CLASS_NAME, 'toast-message')
        #self.assertIn('Aggiunto ddt', toast)
        
        row_manager = RowManager(self)
        row_manager.compile(file_importi)

    def modifica_ddt(self, modifica):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Numero"]/input')
        element.send_keys('01')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        
        self.input(None,'Note').setValue(modifica)

        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()

        self.navigateTo("Ddt in uscita")
        self.wait_loader()    

        self.find(By.XPATH, '//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times fa-2x"]').click()

    def elimina_ddt(self):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()    

        element=self.driver.find_element(By.XPATH,'//th[@id="th_Numero"]/input')
        element.send_keys('02')
        
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys(Keys.ENTER)

        sleep(2)
        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        self.wait_loader()
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]').click()
        self.wait_loader()
        self.find(By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]').click()
        self.wait_loader()