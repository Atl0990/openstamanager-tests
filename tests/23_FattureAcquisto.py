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

class FattureAcquisto(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Acquisti")

    def test_creazione_fattura_acquisto(self):
        # Crea una nuova fattura *Required*
        importi = RowManager.list()
        self.creazione_fattura_acquisto("Fornitore", "1", "1", importi[0])

        # Modifica fattura
        self.modifica_fattura_acquisto("Emessa")
        
        # Controllo valori piano dei conti
        self.controllo_fattura_acquisto()

        # Cancellazione fattura di acquisto
        self.elimina_documento()

    def creazione_fattura_acquisto(self, fornitore: str, numero: str, pagamento: str, file_importi: str):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        # Crea una nuova fattura per il fornitore indicato. 
        # Apre la schermata di nuovo elemento
        self.find(By.CSS_SELECTOR, '#tabs > li:first-child .btn-primary > .fa-plus').click()
        modal = self.wait_modal()

        self.input(modal, 'N. fattura del fornitore').setValue(numero)

        select = self.input(modal, 'Fornitore')
        select.setByText(fornitore)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()
        sleep(1)

        select = self.input(self.find(By.XPATH, '//div[@id="tab_0"]'), 'Pagamento')
        select.setByIndex(pagamento)

        #toast = self.driver.find_elements(By.CLASS_NAME, 'toast-message')
        #self.assertIn('Aggiunto fattura', toast)
        sleep(1)
        row_manager = RowManager(self)
        row_manager.compile(file_importi)

    def modifica_fattura_acquisto(self, modifica=str):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        sleep(1)
        self.find(By.XPATH, '//td[@class="bound clickable"]').click()
        self.wait_loader()
        
        sleep(1)
        self.input(None,'Stato*').setByText(modifica)

        self.find(By.XPATH, '//div[@id="tab_0"]//a[@id="save"]').click()
        self.wait_loader()

    def controllo_fattura_acquisto(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        sleep(1)
        self.find(By.XPATH, '//td[@class="bound clickable"]').click()
        self.wait_loader()
        
        # Estrazione totali righe
        sleep(1)
        sconto = self.find(By.XPATH, '//div[@id="righe"]//tbody[2]//tr[2]//td[2]').text
        totale_imponibile = self.find(By.XPATH, '//div[@id="righe"]//tbody[2]//tr[3]//td[2]').text
        iva = self.find(By.XPATH, '//div[@id="righe"]//tbody[2]//tr[4]//td[2]').text
        totale = self.find(By.XPATH, '//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]').text
        totale='-'+totale

        # Controllo Scadenzario
        scadenza_fattura = self.find(By.XPATH, '//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::p[2]').text
        self.assertEqual(totale, scadenza_fattura[12:21])

        self.driver.execute_script('$("a").removeAttr("target")')
        self.find(By.XPATH, '//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::a').click()
        self.wait_loader()

        scadenza_scadenzario = self.find(By.XPATH, '//div[@id="tab_0"]//td[@id="totale_utente"]').text
        scadenza_scadenzario = scadenza_scadenzario+' €'
        self.assertEqual(totale, scadenza_scadenzario)

        # Torno alla tabella delle Fatture
        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")

        # Estrazione Totale widgets
        widget_fatturato = self.find(By.XPATH, '(//span[@class="info-box-number"])[1]').text
        widget_crediti = self.find(By.XPATH, '(//span[@class="info-box-number"])[2]').text
        widget_crediti='-'+widget_crediti

        # Confronto i due valori
        self.assertEqual(totale_imponibile, widget_fatturato)
        self.assertEqual(totale, widget_crediti)

        # Estrazione valori Piano dei conti
        self.expandSidebar("Contabilità")
        self.navigateTo("Piano dei conti")

        self.find(By.XPATH, '//*[@id="conto3-14"]//*[@class="fa fa-plus"]').click()
        sleep(1) 
        self.find(By.XPATH, '//*[@id="movimenti-55"]//*[@class="fa fa-plus"]').click()
        sleep(1) 
        conto_costi = self.find(By.XPATH, '//*[@id="conto_55"]//*[@class="text-right"]').text
       
        self.find(By.XPATH, '//*[@id="conto3-8"]//*[@class="fa fa-plus"]').click()
        sleep(1)
        self.find(By.XPATH, '//*[@id="movimenti-117"]//*[@class="fa fa-plus"]').click()
        sleep(1) 
        conto_fornitore = self.find(By.XPATH, '//*[@id="conto_117"]//*[@class="text-right"]').text
        conto_fornitore='-'+conto_fornitore

        self.find(By.XPATH, '//*[@id="conto3-22"]//*[@class="fa fa-plus"]').click()
        sleep(1)
        self.find(By.XPATH, '//*[@id="movimenti-107"]//*[@class="fa fa-plus"]').click()        
        sleep(1) 
        conto_iva = self.find(By.XPATH, '//*[@id="conto_107"]//*[@class="text-right"]').text

        self.assertEqual(totale_imponibile, conto_costi)
        self.assertEqual(totale, conto_fornitore)
        self.assertEqual(iva, conto_iva)

    def elimina_documento(self):
        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        sleep(1)
        self.find(By.XPATH, '//td[@class="bound clickable"]').click()
        self.wait_loader()
        self.find(By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]').click()
        self.wait_loader()
        self.find(By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]').click()
        self.wait_loader()

       