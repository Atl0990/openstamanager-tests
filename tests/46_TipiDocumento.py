from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TipiDocumento(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")
        

    def test_creazione_tipi_documento(self):
        # Creazione tipo di documento *Required*
        self.creazione_tipi_documento(descrizione="Tipo di Documento di Prova da Modificare", direzione="Entrata", codice="TD01 - Fattura" )
        self.creazione_tipi_documento(descrizione="Tipo di Documento di Prova da Eliminare", direzione="Entrata", codice="TD01 - Fattura" )

        # Modifica Tipo di documento
        self.modifica_documento("Tipo di Documento di Prova")

        # Cancellazione Tipo di documento
        self.elimina_documento()

        # Verifica Tipo di documento
        self.verifica_tipo_documento()
       
    def creazione_tipi_documento(self, descrizione=str, direzione=str, codice=str):
        self.navigateTo("Tipi documento")
        self.find(By.CSS_SELECTOR, '#tabs > li:first-child .btn-primary > .fa-plus').click()
        modal = self.wait_modal()

        self.input(modal, 'Descrizione').setValue(descrizione)
        select = self.input(modal, 'Direzione')
        select.setByText(direzione)
        select = self.input(modal, 'Codice tipo documento FE')
        select.setByText(codice)

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_documento(self, modifica):
        self.navigateTo("Tipi documento")
        self.wait_loader()

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Tipo di Documento di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click() 
        sleep(1)          

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Descrizione').setValue(modifica)
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()

        self.navigateTo("Tipi documento")
        self.wait_loader()    

        self.find(By.XPATH, '//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times fa-2x"]').click()

    def elimina_documento(self):
        self.navigateTo("Tipi documento")
        self.wait_loader()    

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Tipo di Documento di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()       
        sleep(1) 

        self.driver.execute_script('window.scrollTo(0,0)')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        self.find(By.XPATH, '//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times fa-2x"]').click()

    def verifica_tipo_documento(self):
        self.navigateTo("Tipi documento")
        self.wait_loader()    

        #verifica elemento modificato
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Tipo di Documento di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Tipo di Documento di Prova",modificato)
        self.find(By.XPATH, '//i[@class="deleteicon fa fa-times fa-2x"]').click()

        #verifica elemento eliminato
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Tipo di Documento di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)