from model.database import Database
from model.messaggio import Messaggio
from tkinter import messagebox
from model.fisioterapista import Fisioterapista
import tkinter as tk
from tkinter import scrolledtext

import tkinter.ttk as ttk
from tkinter import font, messagebox, filedialog as fd


from views.messaggi_view import MessaggiView
from views.prenotazione_view import PrenotazioniView

class Paziente:
    def __init__(self, paziente):
        self.paziente = paziente
        self.fisioterapista = Fisioterapista
        self.db = Database()
        self.messaggi_controller = Messaggio()
        

        
#---------------------------------ESERCIZI PAZIENTE---------------------------------------------------------------------

    def visualizza_dettagli_esercizio(self, dettagli, root):
        dettagli_window = tk.Toplevel(root)
        dettagli_window.title(f"Dettagli Esercizio: {dettagli['titolo']}")
        dettagli_window.geometry("900x800")  

        titolo_font = font.Font(family="Arial", size=14, weight="bold")
        testo_font = font.Font(family="Arial", size=14)

        dettagli_frame = tk.Frame(dettagli_window, bg="#f0f0f0")
        dettagli_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titolo_label = tk.Label(dettagli_frame, text=f"Titolo: {dettagli['titolo']}", font=titolo_font, bg="#f0f0f0")
        titolo_label.pack(pady=15)

        descrizione_label = tk.Label(dettagli_frame, text="Descrizione:", font=titolo_font, bg="#f0f0f0")
        descrizione_label.pack(pady=10)

        descrizione_text = tk.Text(dettagli_frame, height=15, width=80, font=testo_font, bg="#ffffff", fg="#333333")
        descrizione_text.pack(pady=10)
        descrizione_text.insert(tk.END, dettagli['descrizione'])
        descrizione_text.config(state=tk.DISABLED)
        
        video_url = tk.Label(dettagli_frame, text=f"Video URL: {dettagli['video_url']}", fg="blue", cursor="hand2")
        video_url.pack(pady=10)
        video_url.bind("<Button-1>", lambda e: self.apri_url(dettagli['video_url']))

        id_paziente = self.db.ottieni_id_paziente(self.paziente.email)

        stato_var = tk.IntVar()
        
        stato_corrente = self.ottieni_stato_esercizio(id_paziente, dettagli['id_esercizio'])
        print("stato ottenuto")
        
        if stato_corrente == 'completato':
            stato_var.set(1)
        else:
            stato_var.set(0)
            
    
        completato_checkbox = tk.Checkbutton(dettagli_frame, text="Esercizio Completato", variable=stato_var, font=testo_font, bg="#f0f0f0")
        completato_checkbox.pack(pady=20)
        
        aggiorna_stato_button = tk.Button(dettagli_frame, text="Aggiorna Stato", command=lambda: self.aggiorna_stato_esercizio(id_paziente, dettagli['id_esercizio'], stato_var),
                                        bg="#4CAF50", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        aggiorna_stato_button.pack(pady=15)
        print("chekbox passata")

        back_button = tk.Button(dettagli_frame, text="Torna Indietro", command=dettagli_window.destroy,
                                bg="#f44336", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        back_button.pack(pady=20)



    def ottieni_esercizi_paziente(self, id_paziente):
        query = '''
        SELECT e.id, e.titolo, e.descrizione, e.video_url
        FROM esercizi e
        INNER JOIN pazienti_esercizi pe ON e.id = pe.id_esercizio
        WHERE pe.id_paziente = ?
        '''
        self.db.cursor.execute(query, (id_paziente,))
        return self.db.cursor.fetchall()
    
    
    
    def ottieni_stato_esercizio(self, id_paziente, id_esercizio):
        self.db.cursor.execute('''
            SELECT stato
            FROM pazienti_esercizi
            WHERE id_paziente = ? AND id_esercizio = ?
        ''', (id_paziente, id_esercizio))
        
        result = self.db.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            return 'incompleto'
        
    def aggiorna_stato_esercizio(self, id_paziente, id_esercizio, stato_var):
        nuovo_stato = 'completato' if stato_var.get() == 1 else 'incompleto'
        
        
        self.db.cursor.execute('''
            UPDATE pazienti_esercizi
            SET stato = ?
            WHERE id_paziente = ? AND id_esercizio = ?
        ''', (nuovo_stato, id_paziente, id_esercizio))
        self.db.conn.commit()
        self.db.calcola_percentuale_completamento(id_paziente)
        messagebox.showinfo("Aggiornamento", "Lo stato dell'esercizio è stato aggiornato.")
        
    def apri_url(self, url):
        import webbrowser
        webbrowser.open(url)
    
        
""" 
    def ottieni_url_video_paziente(self, id_paziente, id_esercizio):
        return self.db.ottieni_url_video_paziente(id_paziente, id_esercizio)
        

    def salva_video_esercizio(self, id_paziente, id_esercizio, percorso_video):
        self.db.cursor.execute('''
            UPDATE pazienti_esercizi
            SET percorso_video = ?
            WHERE id_paziente = ? AND id_esercizio = ?
        ''', (percorso_video, id_paziente, id_esercizio))
        self.db.conn.commit()
        
 """       