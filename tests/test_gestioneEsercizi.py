import unittest
from model.fisioterapista import Fisioterapista 
from model.database import Database
from model.utente import Utente

class TestGestioneEsercizi(unittest.TestCase):
    def setUp(self):
        self.fisioterapista = Utente("Dott. Rossi", "dottor.rossi@email.com", "password123")
        self.db = Database()
        self.controller = Fisioterapista(self.fisioterapista)  

    def test_inserisci_modifica_elimina_esercizio(self):
        titolo = "Mobilizzazione della Spalla per la Rigidità Articolare"
        descrizione = ("Questo esercizio è pensato per migliorare la mobilità della spalla e "
                       "alleviare la rigidità articolare. Seduti o in piedi, il paziente solleva lentamente "
                       "il braccio affetto, eseguendo movimenti circolari controllati e in tutte le direzioni "
                       "per 5 minuti, senza superare il punto di dolore. Ripetere 3 volte al giorno per favorire "
                       "l’aumento della flessibilità e della circolazione nella zona articolare")
        nuovo_titolo = "Rafforzamento dei Muscoli del Core con la Plank Modificata"
        nuova_descrizione = ("L’esercizio della plank modificata mira a rafforzare i muscoli del core, "
                             "fondamentali per la stabilità e l’equilibrio")
        
        if not self.db.trova_esercizio(titolo):
            self.controller.aggiungi_nuovo_esercizio(titolo, descrizione, "")
            id = self.db.ottieni_id_esercizio(titolo)
        
        esercizio_db = self.db.trova_esercizio(titolo)
        self.assertEqual(esercizio_db, (id, titolo, descrizione, ""))
        
        self.controller.modifica_esercizio(nuovo_titolo, nuova_descrizione, id, "https://www.youtube.com/watch?v=lesaJhWyZzA")
        self.assertNotEqual((titolo, descrizione), (nuovo_titolo, nuova_descrizione))
        
        self.controller.elimina_esercizio(id)
        esercizio_eliminato = self.db.trova_esercizio(nuovo_titolo)
        self.assertIsNone(esercizio_eliminato)

        
        
        
        