from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CategorieArticoli(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")

    def test_creazione_categorie_articoli(self):
        # Creazione categoria articoli      *Required*
        self.creazione_categorie_articoli("Categoria Articoli di Prova da Modificare", "#9d2929", "Nota di prova categoria articoli")
        self.creazione_categorie_articoli("Categoria Articoli di Prova da Eliminare", "#9d2929", "Nota di prova categoria articoli")

        # Modifica Categoria Articoli
        self.modifica_categoria_articoli("Categoria Articoli di Prova")
        
        # Cancellazione Categoria Articoli
        self.elimina_categoria_articoli()

        # Verifica Categoria Articoli
        self.verifica_categoria:articoli()

    def creazione_categorie_articoli(self, nome= str, colore=str, nota=str):
        self.navigateTo("Categorie articoli")
        self.find(By.XPATH,'//i[@class="fa fa-plus"]').click()
        modal = self.wait_modal()

        self.input(modal, 'Colore').setValue(colore)
        self.input(modal, 'Nome').setValue(nome)
        self.input(modal, 'Nota').setValue(nota)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_categoria_articoli(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Categorie articoli")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Categoria Articoli di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="module-edit"]//input[@id="nome"]'))).clear()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="module-edit"]//input[@id="nome"]'))).send_keys(modifica, Keys.ENTER)
        sleep(1)
        
        self.navigateTo("Categorie articoli")
        self.wait_loader()    

        self.find(By.XPATH, '//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]').click()

    def elimina_categoria_articoli(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Categorie articoli")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Categoria Articoli di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.find(By.XPATH, '//div[@id="tab_0"]//tbody//td[2]//div[1]').click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()      
                
        self.find(By.XPATH, '//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]').click()

    def verifica_categoria_articoli(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Categorie articoli")
        self.wait_loader()    

        #verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Categoria Articoli di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Categoria Articoli di Prova",modificato)
        self.find(By.XPATH, '//i[@class="deleteicon fa fa-times"]').click()

        #verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Categoria Articoli di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)