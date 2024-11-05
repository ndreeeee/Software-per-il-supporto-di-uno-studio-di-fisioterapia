import sqlite3

class Database:
    def __init__(self, db_name="gestione_fisioterapia.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabella utenti (fisioterapisti e pazienti)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS utenti (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                tipo TEXT NOT NULL CHECK(tipo IN ('fisioterapista', 'paziente'))
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS esercizi (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                titolo TEXT NOT NULL UNIQUE,
                                descrizione TEXT NOT NULL,
                                video_url VARCHAR(255)
                                )''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cartella_clinica (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_paziente INTEGER NOT NULL,
                                data_creazione DATE DEFAULT CURRENT_DATE,
                                data_modifica DATE DEFAULT CURRENT_DATE,
                                descrizione TEXT,
                                FOREIGN KEY (id_paziente) REFERENCES utenti (id) ON DELETE CASCADE
                              )''')
        
        self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS pazienti_esercizi (
                                    id_paziente INTEGER,
                                    id_esercizio INTEGER,
                                    percorso_video TEXT,
                                    stato TEXT DEFAULT 'incompleto' CHECK(stato IN ('completato', 'incompleto')),
                                    data_assegnazione DATE,
                                    data_completamento DATE,
                                    FOREIGN KEY (id_paziente) REFERENCES utenti(id) ON DELETE CASCADE,
                                    FOREIGN KEY (id_esercizio) REFERENCES esercizi(id) ON DELETE CASCADE,
                                    PRIMARY KEY (id_paziente, id_esercizio)
                                );
                            ''')

      
        self.conn.commit()

        

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messaggi (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                mittente_id INTEGER, -- ID del fisioterapista o del paziente
                                destinatario_id INTEGER, -- ID del destinatario (fisioterapista o paziente)
                                messaggio TEXT, -- Il contenuto del messaggio
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- Quando è stato inviato il messaggio
                                visto INTEGER DEFAULT 0, -- Per segnare se il messaggio è stato letto o meno
                                FOREIGN KEY (mittente_id) REFERENCES utenti(id),
                                FOREIGN KEY (destinatario_id) REFERENCES utenti(id));
                            ''')
        
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS prenotazioni (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_paziente INTEGER,
                                id_fisioterapista INTEGER,
                                data_ora DATETIME NOT NULL,
                                stato TEXT DEFAULT 'disponibile' CHECK(stato IN ('disponibile', 'prenotato')),
                                FOREIGN KEY (id_paziente) REFERENCES utenti(id) ON DELETE SET NULL,
                                FOREIGN KEY (id_fisioterapista) REFERENCES utenti (id) ON DELETE SET NULL
                        )''')
        
        self.conn.commit()
        
    def ottieni_messaggi(self):
        self.cursor.execute("SELECT * FROM messaggi")
        return self.cursor.fetchall()
    
    def ottieni_stato_esercizio(self, id_paziente, id_esercizio):
        self.cursor.execute('''
            SELECT stato 
            FROM pazienti_esercizi
            WHERE id_paziente = ? AND id_esercizio = ?
        ''', (id_paziente, id_esercizio))

        risultato = self.cursor.fetchone()
        
        # Se esiste un risultato, restituisci lo stato, altrimenti None
        if risultato:
            return risultato[0]
        else:
            return None

    
    def ottieni_esercizi_pazienti(self):
        self.cursor.execute("SELECT * FROM pazienti_esercizi;")
        return self.cursor.fetchall()
        
    def ottieni_id_paziente(self, email):
        query = "SELECT id FROM utenti WHERE email = ?"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def ottieni_id_esercizio(self,titolo):
        query = "SELECT id FROM esercizi WHERE titolo = ?"
        self.cursor.execute(query, (titolo,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def trova_esercizio(self, titolo):
        self.cursor.execute("SELECT * FROM esercizi WHERE titolo = ?", (titolo,))
        return self.cursor.fetchone()
    
    def aggiungi_utente(self, nome, email, password, tipo):
        self.cursor.execute("INSERT INTO utenti (nome, email, password, tipo) VALUES (?, ?, ?, ?)", 
                            (nome, email, password, tipo))
        self.conn.commit()

    def trova_utente(self, email, password):
        self.cursor.execute("SELECT * FROM utenti WHERE email = ? AND password = ?", (email, password))
        return self.cursor.fetchone()
    
    def ottieni_utenti(self):
        self.cursor.execute("SELECT * FROM utenti")
        return self.cursor.fetchall()

    def ottieni_prenotazioni(self):
        self.cursor.execute("SELECT * FROM prenotazioni")
        return self.cursor.fetchall()
    
    
    def calcola_percentuale_completamento(self, id_paziente):
        # Conta il numero totale di esercizi assegnati
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM pazienti_esercizi
            WHERE id_paziente = ?
        ''', (id_paziente,))
        totale_esercizi = self.cursor.fetchone()[0]

        # Conta il numero di esercizi completati
        self.cursor.execute('''
            SELECT COUNT(*)
            FROM pazienti_esercizi
            WHERE id_paziente = ? AND stato = 'completato'
        ''', (id_paziente,))
        completati = self.cursor.fetchone()[0]

        if totale_esercizi == 0:
            return 0  

        percentuale = (completati / totale_esercizi) * 100
        return percentuale
    
    def trova_cartella_clinica(self, id_paziente):
        self.cursor.execute('''SELECT * FROM cartella_clinica WHERE id_paziente = ?''', (id_paziente,))
        return self.cursor.fetchone()
    
    
    def crea_tabella_prenotazioni(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prenotazioni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paziente INTEGER,
                id_fisioterapista INTEGER,
                data_ora TEXT,
                stato TEXT
            )
        ''')
        self.conn.commit()


    



        
        
    
    
    
      
    
  
  

        
    