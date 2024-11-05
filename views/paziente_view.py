import tkinter as tk
from tkinter import scrolledtext

import tkinter.ttk as ttk
from tkinter import font, messagebox, filedialog as fd


from views.messaggi_view import MessaggiView
from model.paziente import Paziente
from views.prenotazione_view import PrenotazioniView


class PazienteView(tk.Frame):
    def __init__(self, root, paziente):  
        super().__init__(root)  
        self.root = root
        self.paziente = paziente  
        self.controller = Paziente(paziente) 
        
        self.main_frame = tk.Frame(self.root, width=900, height=700)
        self.main_frame.pack_propagate(False) 
        self.main_frame.pack()
        
        button_font = ("Arial", 14, "bold")  

        
        self.spazio = ttk.Label(self.main_frame)
        self.spazio.pack(expand=True)
        
        self.label = ttk.Label(self.main_frame, text=f"Benvenuto, {self.paziente.nome}", font=("Arial", 18, "bold"))
        self.label.pack()
        
        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
        titolo_font = font.Font(family="Arial", size=14, weight="bold")
        
        id_paziente = self.controller.db.ottieni_id_paziente(paziente.email)
        percentuale = self.controller.db.calcola_percentuale_completamento(id_paziente)
        
        percentuale_label = tk.Label(self.main_frame, text=f"Completamento Terapia: {percentuale:.2f}%", font=titolo_font)
        percentuale_label.pack(pady=20)

        progressbar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        progressbar.pack(pady=20)

        progressbar['value'] = percentuale
        
        self.cartella_clinica_btn = ttk.Button(self.main_frame, text="Cartella Clinica", command=self.mostra_cartella_clinica, width=20, style='TButton')
        self.cartella_clinica_btn.pack(pady=20, ipadx=20, ipady=10)

        self.esercizi_btn = ttk.Button(self.main_frame, text="Esercizi", command=self.mostra_esercizi, width=20, style='TButton')
        self.esercizi_btn.pack(pady=20, ipadx=20, ipady=10)

        self.messaggi_btn = ttk.Button(self.main_frame, text="Messaggi", command=self.mostra_messaggi, width=20, style='TButton')
        self.messaggi_btn.pack(pady=20, ipadx=20, ipady=10)
        
        self.messaggi_btn = ttk.Button(self.main_frame, text="Prenotazione", command=self.apri_prenotazioni, width=20, style='TButton')
        self.messaggi_btn.pack(pady=20, ipadx=20, ipady=10)
        
        style = ttk.Style()
        style.configure('TButton', font=button_font)  
        
        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
        

        print("Interfaccia creata con successo")  # Debug per vedere se la GUI è stata creata correttamente

    
      
    
    
# ----------------------------------------------- CARTELLA CLINICA ------------------------------------------------------
    def mostra_cartella_clinica(self):
        print("Mostra cartella clinica chiamato")  # Debug per vedere se il metodo è stato chiamato
        
        cartella_window = tk.Toplevel(self.root)
        cartella_window.title("Cartella Clinica")
        cartella_window.geometry("900x700")

        id_paziente = self.controller.db.ottieni_id_paziente(self.paziente.email)
        cartella_clinica = self.controller.db.trova_cartella_clinica(id_paziente)

        if cartella_clinica:
            id_cartella, id_paziente, data_creazione, data_modifica, descrizione = cartella_clinica
            cartella_info = f"{descrizione}"
            dateModifica = f"\nData di Creazione: {data_creazione}\nData di Modifica: {data_modifica}\n"
            informazioni_label = ttk.Label(cartella_window, text="Cartella Clinica" + dateModifica, font=("Arial", 14))
            informazioni_label.pack(pady=10)
        else:
            cartella_info = "Non hai ancora una cartella clinica."
            informazioni_label = ttk.Label(cartella_window, text="Cartella Clinica", font=("Arial", 14))
            informazioni_label.pack(pady=10)

        descrizione_label = ttk.Label(cartella_window, text="Descrizione", font=("Arial", 14))
        descrizione_label.pack(pady=2)

        info_text = tk.Text(cartella_window, wrap='word', height=20, width=70, font=("Arial", 12))
        info_text.pack(pady=10)

        info_text.insert(tk.END, cartella_info)

        # Imposta la text box come non modificabile
        info_text.config(state=tk.DISABLED)
        
        indietro_button = ttk.Button(cartella_window, text="Torna indietro", command=cartella_window.destroy, style='TButton')
        indietro_button.pack(pady=20, ipadx=20, ipady=10)






# -------------------------------------------------------- ESERCIZI PAZIENTE ------------------------------------------------------


    def mostra_esercizi(self):
        print("Mostra esercizi chiamato")
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Esercizi assegnati")
        search_window.geometry("900x700")  
        
        search_frame = tk.Frame(search_window, width=900, height=700, bg="#f0f0f0")
        search_frame.pack_propagate(False)
        search_frame.pack(pady=20, padx=20)
        
        titolo_font = font.Font(family="Arial", size=16, weight="bold")
        testo_font = font.Font(family="Arial", size=14)
        
        label = tk.Label(search_frame, text="Clicca su un esercizio per vederne i dettagli!", font=titolo_font, bg="#f0f0f0")
        label.pack(pady=10)


        id_paziente = self.controller.db.ottieni_id_paziente(self.paziente.email)
        esercizi = self.controller.ottieni_esercizi_paziente(id_paziente)

        self.esercizi_listbox = tk.Listbox(search_frame, font=testo_font, bg="#ffffff", fg="#333333", height=15, width = 80, bd=2)
        self.esercizi_listbox.pack(pady=20)

        if not esercizi:
            tk.Label(search_frame, text="Nessun esercizio assegnato.", font=titolo_font, bg="#f0f0f0").pack(pady=10)
        else:
            self.esercizi_data = {}
            for esercizio in esercizi:
                id_esercizio = esercizio[0]
                titolo = esercizio[1]
                descrizione = esercizio[2]
                
                self.esercizi_listbox.insert(tk.END, f"{id_esercizio}: {titolo}")
                
                self.esercizi_data[id_esercizio] = {
                    "id_esercizio": esercizio[0],
                    "titolo": titolo,
                    "descrizione": descrizione,
                    "video_url": esercizio[3]
                }

            self.esercizi_listbox.bind("<<ListboxSelect>>", self.mostra_dettagli_esercizio)
        
        
        back_button = tk.Button(search_window, text="Torna Indietro", command=search_window.destroy,
                                bg="#4CAF50", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        back_button.pack()

    def mostra_dettagli_esercizio(self, event):
        try:
            selezione = self.esercizi_listbox.curselection()  
            if selezione:
                indice = selezione[0]
                esercizio_selezionato = self.esercizi_listbox.get(indice) 
                
                id_esercizio = int(esercizio_selezionato.split(":")[0])

                dettagli_esercizio = self.esercizi_data[id_esercizio]

                self.controller.visualizza_dettagli_esercizio(dettagli_esercizio, self.root)
        except Exception as e:
            print(f"Errore durante la visualizzazione dei dettagli dell'esercizio: {e}")

   
    


    """

    def carica_video(self, id_paziente, id_esercizio):
        # Finestra di dialogo per la selezione del file video
        video_file = fd.askopenfilename(title="Seleziona il tuo video di esecuzione", 
                                        filetypes=(("Video Files", "*.mp4;*.avi;*.mov"), ("All Files", "*.*")))
        
        if video_file:
            # Aggiorna la tabella pazienti_esercizi con il percorso del video
            self.controller.salva_video_esercizio(id_paziente, id_esercizio, video_file)
            messagebox.showinfo("Successo", "Il video è stato caricato con successo!")
        else:
            messagebox.showwarning("Errore", "Nessun file selezionato.")
    """
    def apri_url(self, url):
        import webbrowser
        webbrowser.open(url)
    
        
        
# ---------------------------------------------------- MESSAGGI ------------------------------------------------------------------

    def mostra_messaggi(self):
        print("Apertura chat messaggi")
        root = tk.Tk() 
        id_paziente = self.controller.db.ottieni_id_paziente(self.paziente.email)
        self.messaggi = MessaggiView(root, id_paziente, 1, 0)
        
        
#------------------------------------------------------ PRENOTAZIONI --------------------------------------------------------

    def apri_prenotazioni(self):
        self.prenotazioni = PrenotazioniView(self.root, self.paziente, self.controller)


   

