from model.database import Database
from tkinter import messagebox
from backup import backup_database  # Importa la funzione di backup dal file backup.py



class Fisioterapista:
    def __init__(self, fisioterapista):
        self.fisioterapista = fisioterapista
        self.pazienti = []  
        self.db = Database()
        self.carica_pazienti()  
        
        
#-------------------------------------BACKUP-----------------------

    def esegui_backup(self):
        if backup_database() == 1:
            messagebox.showinfo("Successo", "Backup eseguito con successo!")
        else:
            messagebox.showerror("Errore", "Si è verificato un errore durante il backup.")
            
            


#------------------------------------------ CARTELLA CLINICA -----------------------------------------




    def aggiungi_cartella_clinica(self, id, descrizione):
        
        if self.ottieni_cartella_clinica(id):
            messagebox.showerror("Il paziente ha già una cartella clinica!")
            return
        if id and descrizione:
            self.db.cursor.execute('''INSERT INTO cartella_clinica (id_paziente, descrizione) 
                               VALUES (?, ?)''', 
                            (id, descrizione))
            self.db.conn.commit()           
            messagebox.showinfo("Successo", "Cartella Clincia inserita con successo!")
        else:
            messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")
            
            
            
    def modifica_cartella_clinica(self,id_cartella, descrizione):
        self.db.cursor.execute('''UPDATE cartella_clinica 
                               SET descrizione = ?, data_modifica = CURRENT_DATE 
                               WHERE id = ?''', 
                            (descrizione, id_cartella))
        self.db.conn.commit()    
    
    def ottieni_cartella_clinica(self, id_paziente):
        self.db.cursor.execute('''SELECT * FROM cartella_clinica WHERE id_paziente = ?''', (id_paziente,))
        return self.db.cursor.fetchone()
    
    
    
    
    
    
    
    
    
# --------------------------------------------- GESTIONE PAZIENTI ---------------------------------------------


    def carica_pazienti(self):
    # Esegui la query per recuperare i pazienti dalla tabella utenti
        self.pazienti.clear()  # Aggiungi questa riga per svuotare la lista

        self.db.cursor.execute("SELECT id, nome, email FROM utenti WHERE tipo = 'paziente'")
        pazienti_db = self.db.cursor.fetchall()  # Recupera tutti i risultati
        
        # Riempie self.pazienti con i risultati dal database
        for paziente in pazienti_db:
            self.pazienti.append({
                "id": paziente[0],
                "nome": paziente[1],
                "email": paziente[2],
            })
            
    def cerca_pazienti(self, query):
        # Ricerca pazienti per nome o email
        risultati = [
            paziente for paziente in self.pazienti
            if query.lower() in paziente["nome"].lower() or query.lower() in paziente["email"].lower()
        ]
        return risultati

    def aggiungi_paziente(self, nome, email, password):
        # Verifica se l'utente esiste già
        if self.db.trova_utente(email, password):
            messagebox.showerror("Errore", "Esiste già un paziente con questa email.")
            return
        
        # Aggiungi nuovo paziente nel DB
        self.db.cursor.execute("INSERT INTO utenti (nome, email, password, tipo) VALUES (?, ?, ?, 'paziente')", 
                            (nome, email, password))
        
        self.db.conn.commit()
        messagebox.showinfo("Successo", "Paziente aggiunto con successo.")
        
        self.carica_pazienti()
            
    
    def modifica_paziente(self, id_paziente, nome, email, password):
        # Recupera l'email corrente
        self.db.cursor.execute('SELECT email FROM utenti WHERE id = ?', (id_paziente,))
        email_corrente = self.db.cursor.fetchone()

        if email_corrente and email_corrente[0] != email:
            # Se l'email è cambiata, controlla se è già in uso
            self.db.cursor.execute('SELECT * FROM utenti WHERE email = ?', (email,))
            if self.db.cursor.fetchone() is not None:
                messagebox.showerror("Errore", "Esiste già un paziente con questa email.")
                return

        # Procedi con l'aggiornamento
        self.db.cursor.execute('''
            UPDATE utenti
            SET nome = ?, email = ?, password = ?
            WHERE id = ?
        ''', (nome, email, password, id_paziente))
        self.db.conn.commit()
        messagebox.showinfo("Successo", "I dati del paziente sono stati aggiornati")




            
    def elimina_paziente(self, id_paziente):
        # Esegue la query per eliminare il paziente dal database
        self.db.cursor.execute("DELETE FROM utenti WHERE id = ?", (id_paziente,))
        messagebox.showinfo("Successo", "Paziente eliminato con successo.")
        self.db.conn.commit()
         
            
      
    
            


#----------------------------------------- GESTIONE ESERCIZI PAZIENTE --------------------------------------------------------
    def ottieni_esercizi_paziente(self, id_paziente):
        query = '''
        SELECT e.id, e.titolo, e.descrizione, e.video_url
        FROM esercizi e
        INNER JOIN pazienti_esercizi pe ON e.id = pe.id_esercizio
        WHERE pe.id_paziente = ?
        '''
        self.db.cursor.execute(query, (id_paziente,))
        return self.db.cursor.fetchall()
    
    def aggiungi_esercizio_paziente(self, id_paziente, id_esercizio):
    # Aggiunge l'esercizio al paziente, prevenendo duplicati
        self.db.cursor.execute('''INSERT OR IGNORE INTO pazienti_esercizi (id_paziente, id_esercizio) 
                            VALUES (?, ?)''', (id_paziente, id_esercizio))
        self.db.conn.commit()
        
    def ottieni_esercizi(self):
        self.db.cursor.execute("SELECT * FROM esercizi")
        return self.db.cursor.fetchall()
    
    def rimuovi_esercizio_paziente(self, id_esercizio, id_paziente):
     
            # Esegui la query di cancellazione
            self.db.cursor.execute("DELETE FROM pazienti_esercizi WHERE id_esercizio = ? AND id_paziente = ?", (id_esercizio, id_paziente))
            self.db.conn.commit()  # Conferma la modifica
        
    
    
    
    
    
    
    
# ----------------------------------------------------- GESTIONE LISTA ESERCIZI -------------------------------------

            
            
            

    def aggiungi_nuovo_esercizio (self, titolo, descrizione, video_url):
        
        if self.db.trova_esercizio(titolo):
            messagebox.showerror("Errore", "Questo esercizio è stato già inserito")
            return
        
        self.db.cursor.execute("INSERT INTO esercizi (titolo, descrizione, video_url) VALUES (?,?,?)", 
                            (titolo, descrizione, video_url))
        self.db.conn.commit()        
        messagebox.showinfo("Successo", "Esercizio inserito con successo!")
        
    def elimina_esercizio(self, id_esercizio):
        self.db.cursor.execute("DELETE FROM esercizi WHERE id = ?", (id_esercizio,))
        messagebox.showinfo("Successo", "Esercizio eliminato!.")
        self.db.conn.commit()
    
    def modifica_esercizio(self, titolo, descrizione, id_esercizio, url_video):
        self.db.cursor.execute('''
                               UPDATE esercizi
                               SET titolo = ?, descrizione = ?, video_url = ?
                               WHERE id = ?''',
                               (titolo, descrizione, url_video, id_esercizio))
        messagebox.showinfo("Modifiche salvate con successo.")
        self.db.conn.commit()
    
    

  


    
  
    

    
    
    
    
    
    
    

        
        






        






