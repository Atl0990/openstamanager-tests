from common.Test import Test, get_html, get_input
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Anagrafiche(Test):
    def setUp(self):
        super().setUp()

        self.navigateTo("Anagrafiche")

    def test_creazione_cliente(self):
        ''' Crea una nuova anagrafica di tipo Cliente. '''
        self.add_anagrafica('Cliente', 'Cliente', '05024030289')

    def test_creazione_tecnico(self):
        ''' Crea una nuova anagrafica di tipo Tecnico. '''    
        self.add_anagrafica('Tecnico', 'Tecnico', '05024030289')

    def test_creazione_fornitore(self):
        ''' Crea una nuova anagrafica di tipo TecnFornitoreico. '''    
        self.add_anagrafica('Fornitore', 'Fornitore', '05024030289')

    def test_creazione_vettore(self):
        ''' Crea una nuova anagrafica di tipo Vettore. '''    
        self.add_anagrafica('Vettore', 'Vettore', '05024030289')

    def test_creazione_agente(self):
        ''' Crea una nuova anagrafica di tipo Agente. '''    
        self.add_anagrafica('Agente', 'Agente', '05024030289')

    def add_anagrafica(self, name = 'ANAGRAFICA DI PROVA', tipo = 'Cliente', partita_iva = ''):
        ''' Crea una nuova anagrafica del tipo indicato. '''
        # Apre la schermata di nuovo elemento
        self.find(By.CSS_SELECTOR, '.btn-primary > .fa-plus').click()
        modal = self.wait_modal()

        # Completamento dei campi per il nuovo elemento
        get_input(modal, 'Denominazione').send_keys(name)

        modal.find_element(By.CSS_SELECTOR, '.btn-box-tool').click()
        get_input(modal, 'Partita IVA').send_keys(partita_iva)

        select = get_input(modal, 'Tipo di anagrafica')
        select.send_keys(tipo)
        select.send_keys(Keys.ENTER)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()
