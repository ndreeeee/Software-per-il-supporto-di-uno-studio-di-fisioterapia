import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from model.database import Database
from model.prenotazione import Prenotazione
import tkinter.ttk as ttk


class PrenotazioniView(tk.Toplevel):
    def __init__(self, root, paziente, controller):
        super().__init__(root)
        self.controller = Prenotazione() 
        self.title("Prenotazioni disponibili")
        self.geometry("900x700")  
        self.paziente = paziente
        self.pazienteController = controller

        self.prenotazioni_effettuate_lista = ttk.Treeview(self, columns=("ID", "Data e Ora", "Stato"), show="headings")
        self.prenotazioni_effettuate_lista.heading("ID", text="ID")
        self.prenotazioni_effettuate_lista.heading("Data e Ora", text="Data e Ora")
        self.prenotazioni_effettuate_lista.heading("Stato", text="Stato")
        self.prenotazioni_effettuate_lista.column("ID", width=100)  
        self.prenotazioni_effettuate_lista.column("Data e Ora", width=200) 
        self.prenotazioni_effettuate_lista.column("Stato", width=100)  
        self.prenotazioni_effettuate_lista.pack(fill=tk.BOTH, expand=True, pady=10)

        self.cancella_prenotazione_effettuata_btn = ttk.Button(self, text="Cancella Prenotazione Effettuata", command=self.cancella_prenotazione_effettuata)
        self.cancella_prenotazione_effettuata_btn.pack(pady=10)

        self.prenotazioni_lista = ttk.Treeview(self, columns=("ID", "Data e Ora", "Stato"), show="headings")
        self.prenotazioni_lista.heading("ID", text="ID")
        self.prenotazioni_lista.heading("Data e Ora", text="Data e Ora")
        self.prenotazioni_lista.heading("Stato", text="Stato")
        self.prenotazioni_lista.column("ID", width=100) 
        self.prenotazioni_lista.column("Data e Ora", width=200)  
        self.prenotazioni_lista.column("Stato", width=100)  
        self.prenotazioni_lista.pack(fill=tk.BOTH, expand=True)

        self.prenota_btn = ttk.Button(self, text="Prenota", command=self.prenota)
        self.prenota_btn.pack(pady=10)

        self.torna_indietro_btn = ttk.Button(self, text="Torna Indietro", command=self.torna_indietro)
        self.torna_indietro_btn.pack(pady=10)

        self.controller.elimina_prenotazioni_scadute()
        self.carica_prenotazioni_disponibili()
        self.carica_prenotazioni_effettuate()

    def carica_prenotazioni_disponibili(self):
        print("Caricamento prenotazioni disponibili")
        for item in self.prenotazioni_lista.get_children():
            self.prenotazioni_lista.delete(item)

        prenotazioni = self.controller.visualizza_prenotazioni_disponibili()

        for prenotazione in prenotazioni:
            print(prenotazione)
            self.prenotazioni_lista.insert('', 'end', values=(prenotazione[0], prenotazione[3], prenotazione[4]))

    def carica_prenotazioni_effettuate(self):
        print("Caricamento prenotazioni effettuate")
        for item in self.prenotazioni_effettuate_lista.get_children():
            self.prenotazioni_effettuate_lista.delete(item)

        id_paziente = self.pazienteController.db.ottieni_id_paziente(self.paziente.email)
        prenotazioni = self.controller.visualizza_prenotazioni_paziente(id_paziente)

        for prenotazione in prenotazioni:
            self.prenotazioni_effettuate_lista.insert('', 'end', values=(prenotazione[0], prenotazione[3], prenotazione[4]))

    def prenota(self):
        selected_item = self.prenotazioni_lista.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Seleziona una prenotazione")
            return

        prenotazione = self.prenotazioni_lista.item(selected_item)['values']
        print("Prenotazione selezionata:", prenotazione)

        prenotazione_id = prenotazione[0]
        data_ora = prenotazione[1]  
        id_paziente = self.pazienteController.db.ottieni_id_paziente(self.paziente.email)

        try:
            self.controller.aggiungi_prenotazione(id_paziente, prenotazione_id, data_ora)
            messagebox.showinfo("Successo", "Prenotazione avvenuta con successo!")
            self.carica_prenotazioni_disponibili()
            self.carica_prenotazioni_effettuate()  
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def cancella_prenotazione_effettuata(self):
        selected_item = self.prenotazioni_effettuate_lista.selection()
        if not selected_item:
            messagebox.showerror("Errore", "Seleziona una prenotazione da cancellare")
            return

        prenotazione = self.prenotazioni_effettuate_lista.item(selected_item)['values']
        prenotazione_id = prenotazione[0]

        risposta = messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare la prenotazione?")
        if risposta:
            try:
                self.controller.rimuovi_prenotazione(prenotazione_id)

                self.prenotazioni_effettuate_lista.delete(selected_item)

                self.carica_prenotazioni_disponibili()  

                messagebox.showinfo("Successo", "Prenotazione cancellata e ora disponibile!")
            except Exception as e:
                messagebox.showerror("Errore", str(e))

    def torna_indietro(self):
        self.destroy()  # Chiude la finestra attuale
