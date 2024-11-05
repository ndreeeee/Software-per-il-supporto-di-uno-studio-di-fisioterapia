from model.database import Database
from model.utente import Fisioterapista, Paziente
from views.fisioterapista_view import FisioterapistaView
from views.paziente_view import PazienteView
import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root = root
        self.db = Database()

    def controlla_login(self, email, password):
        utente = self.db.trova_utente(email, password)
        if utente:
            _, nome, email, password, tipo = utente
            if tipo == "fisioterapista":
                self.carica_fisioterapista_view(nome, email, password)
            elif tipo == "paziente":
                self.carica_paziente_view(nome, email, password)
        else:
            messagebox.showerror("Errore", "Email o password errati")
            

    def carica_fisioterapista_view(self, nome, email, password):
        fisioterapista = Fisioterapista(nome, email, password)
        self.root.destroy() 
        root = tk.Tk() 
        FisioterapistaView(root, fisioterapista).pack()

    def carica_paziente_view(self, nome, email, password):
        paziente = Paziente(nome, email, password)
        self.root.destroy()  
        root = tk.Tk()  
        paziente_view = PazienteView(root, paziente)  
        paziente_view.pack()  
