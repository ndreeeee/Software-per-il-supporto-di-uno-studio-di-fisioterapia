import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from model.database import Database

class Prenotazione:
    def __init__(self):
        self.db = Database()
        self.aggiorna_prenotazioni_future(giorni_in_avanti=7)
    
    def aggiorna_prenotazioni_future(self, giorni_in_avanti=7):
        """
        Crea nuove prenotazioni con stato 'disponibile' fino a una certa data nel futuro,
        saltando sabato e domenica.
        """
        self.db.cursor.execute('SELECT MAX(data_ora) FROM prenotazioni')
        ultima_data = self.db.cursor.fetchone()[0]

       
        if ultima_data is None:
            ultima_data = datetime.now()
        else:
            ultima_data = datetime.strptime(ultima_data, '%Y-%m-%d %H:%M')

        # Determina la data limite per le nuove prenotazioni
        data_limite = datetime.now() + timedelta(days=giorni_in_avanti)

        while ultima_data < data_limite:
            ultima_data += timedelta(days=1)
            # per togliere sabato e domenica
            if ultima_data.weekday() in [5, 6]:
                continue
            self.riempi_prenotazioni_iniziali(ultima_data.date(), '09:00', '18:00', id_fisioterapista=1)

    def riempi_prenotazioni_iniziali(self, data, orario_inizio, orario_fine, id_fisioterapista):
        
        ora_inizio = datetime.strptime(orario_inizio, "%H:%M").time()
        ora_fine = datetime.strptime(orario_fine, "%H:%M").time()
        orario_corrente = datetime.combine(data, ora_inizio)

        while orario_corrente.time() <= ora_fine:
            data_ora = orario_corrente.strftime('%Y-%m-%d %H:%M')
            self.db.cursor.execute('''
                INSERT INTO prenotazioni (id_paziente, id_fisioterapista, data_ora, stato)
                VALUES (NULL, ?, ?, 'disponibile')
            ''', (id_fisioterapista, data_ora))
            orario_corrente += timedelta(hours=1)

        self.db.conn.commit()

    
    def visualizza_prenotazioni_paziente(self, id_paziente):
        self.db.cursor.execute(''' 
            SELECT * FROM prenotazioni 
            WHERE id_paziente = ? 
        ''', (id_paziente,))
        return self.db.cursor.fetchall()  


    def visualizza_prenotazioni_fisioterapista(self):
        
        self.db.cursor.execute('SELECT * FROM prenotazioni;')
        self.db.cursor.execute('''
            SELECT prenotazioni.id, utenti.nome, prenotazioni.data_ora
            FROM prenotazioni
            JOIN utenti ON prenotazioni.id_paziente = utenti.id
        ''')

        return self.db.cursor.fetchall()

    def rimuovi_prenotazione(self, prenotazione_id):
        self.db.cursor.execute('''
            UPDATE prenotazioni
            SET stato = 'disponibile',
                id_paziente = NULL
            WHERE id = ?
        ''', (prenotazione_id,))
        self.db.conn.commit()

    def visualizza_prenotazioni_disponibili(self):
        self.db.cursor.execute('''
            SELECT * FROM prenotazioni
            WHERE stato = 'disponibile'
        ''')
        return self.db.cursor.fetchall()
    


    def aggiungi_prenotazione(self, id_paziente, id_prenotazione, data_ora): 
        print(f"Tentativo di aggiungere prenotazione con id_paziente={id_paziente}, id_prenotazione={id_prenotazione}, data_ora={data_ora}")
        
        self.db.cursor.execute('''
                UPDATE prenotazioni
                SET id_paziente = ?, stato = 'prenotato'
                WHERE id = ? AND data_ora = ? AND stato = 'disponibile'
            ''', (id_paziente, id_prenotazione, data_ora))
        self.db.conn.commit()

        print("Righe aggiornate:", self.db.cursor.rowcount)

       
        
    def modifica_stato_prenotazione(self, prenotazione_id, nuovo_stato):
        self.db.cursor.execute('''
            UPDATE prenotazioni
            SET stato = ?
            WHERE id = ?
        ''', (nuovo_stato, prenotazione_id))
        self.db.conn.commit()
        
    def elimina_prenotazioni_scadute(self):
        data_ora_attuale = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.db.cursor.execute('''
            DELETE FROM prenotazioni
            WHERE data_ora < ? 
        ''', (data_ora_attuale,))
        self.db.conn.commit()
        
        
"""def __init__(self):
        self.db = Database()
        self.check_popola_prenotazioni()

    def check_popola_prenotazioni(self):
        
        # Controlla se ci sono prenotazioni già nel database
        self.db.cursor.execute('SELECT COUNT(*) FROM prenotazioni')
        count = self.db.cursor.fetchone()[0]

        if count == 0:
            # Se il database è vuoto, crea prenotazioni disponibili
            print("Popolamento del database con prenotazioni iniziali.")
            self.riempi_prenotazioni_iniziali('09:00', '18:00', 7, 1)
        
        
    def riempi_prenotazioni_iniziali(self, orario_inizio, orario_fine, giorni_da_oggi, id_fisioterapista):
      
        ora_inizio = datetime.strptime(orario_inizio, "%H:%M").time()
        ora_fine = datetime.strptime(orario_fine, "%H:%M").time()
        today = datetime.now()

        for giorno in range(giorni_da_oggi):
            data_corrente = today + timedelta(days=giorno)
            orario_corrente = datetime.combine(data_corrente.date(), ora_inizio)
            
            

            while orario_corrente.time() <= ora_fine:
                data_ora = orario_corrente.strftime('%Y-%m-%d %H:%M')
                self.db.cursor.execute('''
                    INSERT INTO prenotazioni (id_paziente, id_fisioterapista, data_ora, stato)
                    VALUES (NULL, ?, ?, 'disponibile')
                ''', (id_fisioterapista, data_ora))
                
                # Aggiungi 1 ora tra una prenotazione e l'altra
                orario_corrente += timedelta(hours=1)

        self.db.conn.commit()"""
        
    
