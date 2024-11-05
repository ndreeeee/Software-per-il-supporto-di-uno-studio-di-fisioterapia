import sqlite3
from datetime import datetime


class Messaggio:
    def __init__(self, db_name="gestione_fisioterapia.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def invia_messaggio(self, mittente_id, destinatario_id, testo):
        """Inserisce un nuovo messaggio nel database."""
        self.cursor.execute('''
            INSERT INTO messaggi (mittente_id, destinatario_id, messaggio, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (mittente_id, destinatario_id, testo, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        
    def ottieni_nome_utente(self, utente_id):
        query = "SELECT nome FROM utenti WHERE id = ?"
        nome = self.cursor.execute(query, (utente_id,)).fetchone()
        print(f"ID Utente: {utente_id}, Nome: {nome}")  
        return nome[0]

    def visualizza_messaggi(self, paziente_id, fisioterapista_id):
        query = '''
        SELECT mittente_id, messaggio, timestamp
        FROM messaggi
        WHERE (mittente_id = ? AND destinatario_id = ?)
           OR (mittente_id = ? AND destinatario_id = ?)
        ORDER BY timestamp ASC
        '''
        return self.cursor.execute(query, (paziente_id, fisioterapista_id, fisioterapista_id, paziente_id)).fetchall()

    def close(self):
        """Chiude la connessione al database."""
        self.conn.close()