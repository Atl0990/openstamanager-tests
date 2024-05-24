from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Eventi(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")
       

    def test_creazione_eventi(self):
        # Creazione evento *Required*
        self.creazione_eventi("Evento di Prova da Modificare", "20/02/2024", "IT - Italia")
        self.creazione_eventi("Evento di Prova da Eliminare", "20/02/2024", "IT - Italia")

        # Modifica Evento
        self.modifica_evento("Evento di Prova")
        
        # Cancellazione Evento
        self.elimina_evento()
        
        # Verifica Evento
        self.verifica_evento()

    def creazione_eventi(self, nome=str, data=str, nazione=str):
        self.navigateTo("Eventi")
        self.find(By.XPATH,'//i[@class="fa fa-plus"]').click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue(nome)   
        self.input(None, 'Data').setValue(data)
        select = self.input(modal, 'Nazione')
        select.setByText(nazione)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_evento(self, modifica):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Eventi")
        self.wait_loader()
     
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Evento di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()    
        sleep(1)    

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Nome').setValue(modifica)
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()

        self.navigateTo("Eventi")
        self.wait_loader()    

        self.find(By.XPATH, '//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]').click()

    def elimina_evento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Eventi")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Evento di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()     
        sleep(1)      

        self.driver.execute_script('window.scrollTo(0,0)')

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1) 

        self.find(By.XPATH, '//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]').click()   

    def verifica_evento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Eventi")
        self.wait_loader()    

        #verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Evento di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Evento di Prova",modificato)
        self.find(By.XPATH, '//i[@class="deleteicon fa fa-times"]').click()

        #verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Evento di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)