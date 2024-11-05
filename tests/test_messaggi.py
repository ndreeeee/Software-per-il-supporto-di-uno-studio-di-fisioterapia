import unittest
from model.messaggio import Messaggio
from model.database import Database
from model.utente import Utente

class TestGestioneMessaggi(unittest.TestCase):
    def setUp(self):
        self.db = Database(db_name="test_gestione_fisioterapia.db")  
        self.controller = Messaggio(db_name="test_gestione_fisioterapia.db")
    
        self.db.aggiungi_utente("Dott. Rossi", "dottor.rossi@email.com", "password123", "fisioterapista")
        self.db.aggiungi_utente("Mario Neri", "mario.neri@email.com", "password123", "paziente")

        self.fisioterapista_id = self.db.ottieni_id_paziente("dottor.rossi@email.com")
        self.paziente_id = self.db.ottieni_id_paziente("mario.neri@email.com")
        
    def test_invio_e_visualizzazione_messaggi(self):
        testo_messaggio = "Ciao Mario, ricordati dell'appuntamento di domani."
        self.controller.invia_messaggio(self.fisioterapista_id, self.paziente_id, testo_messaggio)
        
        messaggi = self.controller.visualizza_messaggi(self.paziente_id, self.fisioterapista_id)
        self.assertTrue(any(m[1] == testo_messaggio for m in messaggi))
        
        risposta_messaggio = "Grazie dottore, sarò presente."
        self.controller.invia_messaggio(self.paziente_id, self.fisioterapista_id, risposta_messaggio)
        
        messaggi = self.controller.visualizza_messaggi(self.paziente_id, self.fisioterapista_id)
        self.assertEqual(len(messaggi), 2)
        self.assertIn(testo_messaggio, [m[1] for m in messaggi])
        self.assertIn(risposta_messaggio, [m[1] for m in messaggi])

    def tearDown(self):
        self.db.cursor.execute("DROP TABLE IF EXISTS messaggi")
        self.db.cursor.execute("DROP TABLE IF EXISTS utenti")
        self.db.conn.commit()
        self.controller.close()
        self.db.conn.close()
