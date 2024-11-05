import unittest
from model.fisioterapista import Fisioterapista 
from model.database import Database
from model.utente import Utente

class TestGestionePazienti(unittest.TestCase):
    def setUp(self):
        self.fisioterapista = Utente("Dott. Rossi", "dottor.rossi@email.com", "password123")
        self.db = Database()
        self.controller = Fisioterapista(self.fisioterapista)  

    
    def test_inserisci_modifica_elimina_paziente(self):
        nome = "Mario Bianchi"
        email = "mb@gmail.com" 
        password = "pratofiorito"
        
        if not self.db.trova_utente(email, password):
            self.controller.aggiungi_paziente(nome,email, password)
            id = self.db.ottieni_id_paziente(email)
            
        self.assertEqual(self.db.trova_utente(email, password), (id, nome, email, password, 'paziente'))
        
        self.controller.modifica_paziente(id, "Mario Neri", "mn@gmail.com", "prato")
        self.assertNotEqual((nome, email, password), ("Mario Neri", "mn@gmail.com", "prato"))
        
        self.controller.elimina_paziente(id)
        self.assertIsNone(self.db.trova_utente("mn@gmail.com", "prato"))
        
        
        
        
        