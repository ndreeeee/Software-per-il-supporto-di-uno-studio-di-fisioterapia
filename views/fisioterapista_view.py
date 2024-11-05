import tkinter as tk

from tkinter import scrolledtext  
import tkinter.ttk as ttk
from tkinter import font, messagebox, simpledialog, filedialog


from model.fisioterapista import Fisioterapista
from model.prenotazione import Prenotazione
from views.messaggi_view import MessaggiView


# width=700, height=600
class FisioterapistaView(tk.Frame):
    def __init__(self, root, fisioterapista):
        self.root = root
        self.fisioterapista = fisioterapista
        self.controller = Fisioterapista(fisioterapista)
        self.prenotazione_controller = Prenotazione()
        self.file_video_path = ""

        self.main_frame = tk.Frame(self.root, width=900, height=700)
        self.main_frame.pack_propagate(False)  
        self.main_frame.pack()
        
        # per centrare verticalmente assieme a spazio2
        self.spazio = tk.Label(self.main_frame)
        self.spazio.pack(expand=True)

        self.label = ttk.Label(self.main_frame, text=f"Benvenuto, {self.fisioterapista.nome}", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)
        
        button_font = ("Arial", 14, "bold") 

        self.cerca_pazienti_button = ttk.Button(self.main_frame, text="Cerca Paziente", command=lambda: self.mostra_form_cerca_paziente(0), 
                                                width=20, style='TButton')
        self.cerca_pazienti_button.pack(pady=20, ipadx=20, ipady=10)

        self.aggiungi_paziente_button = ttk.Button(self.main_frame, text="Aggiungi Paziente", command=self.mostra_form_aggiungi_paziente, width=20, style='TButton')
        self.aggiungi_paziente_button.pack(pady=20, ipadx=20, ipady=10)
        
        self.mostra_esercizi_button = ttk.Button(self.main_frame, text="Lista Esercizi", command=self.mostra_lista_esercizi, width=20, style='TButton')
        self.mostra_esercizi_button.pack(pady=20, ipadx=20, ipady=10)

        self.prenotazione_button = ttk.Button(self.main_frame, text="Prenotazioni", command=self.mostra_prenotazioni, width=20, style='TButton')
        self.prenotazione_button.pack(pady=20, ipadx=20, ipady=10)
        
        self.messaggia_paziente_button = ttk.Button(self.main_frame, text="Messaggia Paziente", command=lambda: self.mostra_form_cerca_paziente(1), width=20, style='TButton')
        self.messaggia_paziente_button.pack(pady=20, ipadx=20, ipady=10)
        
        self.esegui_backup_ = ttk.Button(self.main_frame, text="Esegui Backup", command=self.controller.esegui_backup, width=20, style='TButton')
        self.esegui_backup_.pack(pady=20, ipadx=20, ipady=10)

     
        style = ttk.Style()
        style.configure('TButton', font=button_font)  
        
        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
#-------------------------------------- CARTELLA CLINICA ----------------------------------------------------


    
    
    
    
    def mostra_cartella_clinica(self, paziente):
    
        cartella_window = tk.Toplevel(self.root)
        cartella_window.title("Cartella Clinica")
        cartella_window.geometry("900x700")
        cartella_clinica = self.controller.ottieni_cartella_clinica(paziente)

        if cartella_clinica:
            id_cartella, id_paziente, data_creazione, data_modifica, descrizione = cartella_clinica
            cartella_info = f"{descrizione}"
            dateModifica = f"\nData di Creazione: {data_creazione}\nData di Modifica: {data_modifica}\n"
            informazioni_label = ttk.Label(cartella_window, text="Cartella Clinica del Paziente" + dateModifica, font=("Arial", 14))
            informazioni_label.pack(pady=10)
        else:
            cartella_info = "Il paziente non ha ancora una cartella clinica."
            informazioni_label = ttk.Label(cartella_window, text="Cartella Clinica del Paziente", font=("Arial", 14))
            informazioni_label.pack(pady=10)

        descrizione_label = ttk.Label(cartella_window, text="Descrizione", font=("Arial", 14))
        descrizione_label.pack(pady=2)

        info_text = tk.Text(cartella_window, wrap='word', height=20, width=70, font=("Arial", 12))
        info_text.pack(pady=10)

        info_text.insert(tk.END, cartella_info)
        

        def salva_modifiche(flag):
            testo_modificato = info_text.get("1.0", tk.END).strip()  
            
            if flag == 1:
                try:
                    self.controller.aggiungi_cartella_clinica(paziente, testo_modificato)
                    cartella_window.destroy

                except Exception as e:
                    messagebox.showerror("Errore", f"Si è verificato un errore durante l'esecuzione: {e}")
            else:
                if not testo_modificato:
                    messagebox.showwarning("Attenzione", "Nessun testo da salvare.")
                    return
                try:
                    self.controller.modifica_cartella_clinica(id_cartella, testo_modificato)  
                    messagebox.showinfo("Successo", "Modifiche salvate con successo!")
                    cartella_window.destroy
                except Exception as e:
                    messagebox.showerror("Errore", f"Si è verificato un errore durante il salvataggio: {e}")

        if cartella_clinica:
            salva_button = ttk.Button(cartella_window, text="Salva Modifiche", command=lambda: salva_modifiche(0), style='TButton')
            salva_button.pack(pady=20, ipadx=20, ipady=10)
        else:
            aggiungi_button = ttk.Button(cartella_window, text="Aggiungi cartella clinica", command=lambda: salva_modifiche(1), style='TButton')
            aggiungi_button.pack(pady=20, ipadx=20, ipady=10)
            
        indietro_button = ttk.Button(cartella_window, text="Torna indietro", command=cartella_window.destroy, style='TButton')
        indietro_button.pack(pady=20, ipadx=20, ipady=10)
        




        
        

        
        
        
# --------------------------------------------- GESTIONE PAZIENTI ---------------------------------------------
        
    def mostra_form_cerca_paziente(self, flag):
        search_window = tk.Toplevel(self.root)
        search_window.title("Cerca Paziente")

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12, "bold"))

        search_frame = ttk.Frame(search_window, width=900, height=700)
        search_frame.pack_propagate(False) 
        search_frame.pack(pady=20, padx=20)  

        
        ttk.Label(search_frame, text="Inserisci il nome o cognome del paziente", style="TLabel").pack(pady=10)

     
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 14), width=40)
        self.search_entry.pack(pady=10)

      
        self.search_entry.bind("<KeyRelease>", self.aggiorna_ricerca)
        
        self.results_listbox = tk.Listbox(search_frame, width=80, height=20, font=("Arial", 14))  
        self.results_listbox.pack(pady=10)

        back_button = ttk.Button(search_frame, text="Torna Indietro", command=search_window.destroy, style="TButton")
        back_button.pack(pady=20, ipadx=10, ipady=5)  

        self.visualizza_tutti_pazienti()  
        
        if flag == 1:
            self.results_listbox.bind("<Double-1>", self.apri_chat_paziente)
        
    def mostra_form_modifica_paziente(self, paziente, finestra):
        
        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modifica Paziente")

        modify_frame = ttk.Frame(modify_window, width=900, height=700)
        modify_frame.pack_propagate(False)
        modify_frame.pack(pady=20, padx=20)  


        ttk.Label(modify_frame, text="Nome Paziente", font=("Arial", 16)).pack(pady=5)
        nome_entry = ttk.Entry(modify_frame, font=("Arial", 14), width=70)
        nome_entry.insert(0, paziente['nome']) 
        nome_entry.pack(pady=10)

        ttk.Label(modify_frame, text="Email Paziente", font=("Arial", 16)).pack(pady=5)
        email_entry = ttk.Entry(modify_frame, font=("Arial", 14), width=70)
        email_entry.insert(0, paziente['email']) 
        email_entry.pack(pady=10)

        ttk.Label(modify_frame, text="Password Paziente", font=("Arial", 16)).pack(pady=5)
        password_entry = ttk.Entry(modify_frame, show="*", font=("Arial", 14), width=70)  
        password_entry.pack(pady=10)

       
        submit_button = ttk.Button(modify_frame, text="Salva Modifiche", 
                                command=lambda: self.modifica_paziente(paziente['id'], nome_entry.get(), email_entry.get(), password_entry.get(), modify_window, finestra),
                                style="TButton")
        submit_button.pack(pady=15, ipadx=10, ipady=5)

      
        back_button = ttk.Button(modify_frame, text="Torna Indietro", command=modify_window.destroy, style="TButton")
        back_button.pack(pady=10, ipadx=10, ipady=5)
        
    def modifica_paziente(self, id_paziente, nome, email, password, window, finestra):
        if nome and email and password:
          
            self.controller.modifica_paziente(id_paziente, nome, email, password)
            self.visualizza_tutti_pazienti()             
        else:
            messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")
            
        window.destroy() 
        finestra.destroy() 
        
    def aggiungi_paziente(self, nome, email, password, window):
        if nome and email and password:
            self.controller.aggiungi_paziente(nome, email, password)
            self.visualizza_tutti_pazienti() 

            window.destroy() 
        else:
            messagebox.showerror("Errore", "Tutti i campi sono obbligatori!")


    def visualizza_tutti_pazienti(self):
        self.results_listbox.delete(0, tk.END)
        for paziente in self.controller.pazienti:
            self.results_listbox.insert(tk.END, f"ID: {paziente['id']}, Nome: {paziente['nome']}, Email: {paziente['email']}")

        self.results_listbox.bind("<Double-1>", self.apri_profilo_paziente)

        
    def mostra_form_aggiungi_paziente(self):
        
        form_window = tk.Toplevel(self.root)
        form_window.title("Aggiungi Nuovo Paziente")

        self.main_frame = ttk.Frame(form_window, width=900, height=700)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(pady=20, padx=20)

        self.spazio = ttk.Label(self.main_frame)
        self.spazio.pack(expand=True)

        # Campo per inserire il nome del paziente
        ttk.Label(self.main_frame, text="Nome Paziente", font=("Arial", 16)).pack(pady=5)
        nome_entry = ttk.Entry(self.main_frame, font=("Arial", 14), width=70)
        nome_entry.pack(pady=10)

        # Campo per inserire l'email del paziente
        ttk.Label(self.main_frame, text="Email Paziente", font=("Arial", 16)).pack(pady=5)
        email_entry = ttk.Entry(self.main_frame, font=("Arial", 14), width=70)
        email_entry.pack(pady=10)

        # Campo per inserire la password del paziente
        ttk.Label(self.main_frame, text="Password Paziente", font=("Arial", 16)).pack(pady=5)
        password_entry = ttk.Entry(self.main_frame, show="*", font=("Arial", 14), width=70)
        password_entry.pack(pady=10)

        # Pulsante per aggiungere il paziente
        submit_button = ttk.Button(self.main_frame, text="Aggiungi", 
                                command=lambda: self.aggiungi_paziente(nome_entry.get(), email_entry.get(), password_entry.get(), form_window),
                                style="TButton")
        submit_button.pack(pady=15, ipadx=10, ipady=5)

        # Pulsante per tornare indietro
        back_button = ttk.Button(self.main_frame, text="Torna Indietro", command=form_window.destroy, style="TButton")
        back_button.pack(pady=10, ipadx=10, ipady=5)

        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
    def apri_profilo_paziente(self, event):
        indice_selezionato = self.results_listbox.curselection()
        if indice_selezionato:
            
            paziente = self.controller.pazienti[indice_selezionato[0]]

            search_frame = tk.Toplevel(self.root)
            search_frame.title(f"Profilo di {paziente['nome']}")

            profilo_paziente_window = ttk.Frame(search_frame, width=900, height=700)
            profilo_paziente_window.pack_propagate(False)
            profilo_paziente_window.pack(pady=20, padx=20)

            self.spazio = ttk.Label(profilo_paziente_window)
            self.spazio.pack(expand=True)
            
            button_font = ("Arial", 14, "bold")  # Font più grande e in grassetto

            ttk.Label(profilo_paziente_window, text=f"Nome: {paziente['nome']}", font=("Arial", 12, 'bold')).pack(pady=10)
            ttk.Label(profilo_paziente_window, text=f"Email: {paziente['email']}", font=("Arial", 12)).pack(pady=10)
            
            titolo_font = font.Font(family="Arial", size=14, weight="bold")
            testo_font = font.Font(family="Arial", size=12)
            
            id_paziente = self.controller.db.ottieni_id_paziente(paziente['email'])
            percentuale = self.controller.db.calcola_percentuale_completamento(id_paziente)
            
            percentuale_label = tk.Label(profilo_paziente_window, text=f"Completamento Terapia: {percentuale:.2f}%", font=titolo_font)
            percentuale_label.pack(pady=20)

            progressbar = ttk.Progressbar(profilo_paziente_window, orient="horizontal", length=300, mode="determinate")
            progressbar.pack(pady=20)

            progressbar['value'] = percentuale

            ttk.Button(profilo_paziente_window, text="Cartella Clinica", 
                    command=lambda: self.mostra_cartella_clinica(paziente['id']), style="TButton").pack(pady=20, ipadx=20, ipady=10)
            ttk.Button(profilo_paziente_window, text="Gestisci Esercizi", 
                    command=lambda: self.gestisci_esercizi(paziente['id']), style="TButton").pack(pady=20, ipadx=20, ipady=10)

            ttk.Button(profilo_paziente_window, text="Modifica Paziente", 
                    command=lambda: self.mostra_form_modifica_paziente(paziente, search_frame), style="TButton").pack(pady=20, ipadx=20, ipady=10)
            
            ttk.Button(profilo_paziente_window, text="Elimina Paziente", 
                    command=lambda: self.elimina_paziente(id_paziente, search_frame), style="TButton").pack(pady=20, ipadx=20, ipady=10)

            ttk.Button(profilo_paziente_window, text="Torna Indietro", 
                    command=search_frame.destroy, style="TButton").pack(pady=20, ipadx=20, ipady=10)

            style = ttk.Style()
            style.configure('TButton', font=button_font) 
            self.spazio2 = ttk.Label(profilo_paziente_window)
            self.spazio2.pack(expand=True)
            
    def elimina_paziente(self, id_paziente, finestra_profilo):
        risposta = messagebox.askyesno("Conferma Eliminazione", "Sei sicuro di voler eliminare questo paziente?")
        
        if risposta:
            self.controller.elimina_paziente(id_paziente)
            self.visualizza_tutti_pazienti()  

            finestra_profilo.destroy()            
    
    def aggiorna_ricerca(self, event):
        query = self.search_entry.get().strip()  
        if query:
            
            risultati = self.controller.cerca_pazienti(query)
            self.results_listbox.delete(0, tk.END)

            if risultati:
                for paziente in risultati:
                    try:
                        
                        self.results_listbox.insert(tk.END, f"ID: {paziente['id']}, Nome: {paziente['nome']}, Email: {paziente['email']}")
                    except KeyError:
                        self.results_listbox.insert(tk.END, "Dati paziente non validi.")
            else:
                self.results_listbox.insert(tk.END, "Nessun paziente trovato.")
        else:
            self.visualizza_tutti_pazienti()  





#----------------------------------------- GESTIONE ESERCIZI PAZIENTE --------------------------------------------------------
            
    
    
    
    
    def gestisci_esercizi(self, id_paziente):
        profilo_paziente_window = tk.Toplevel(self.root)
        profilo_paziente_window.title("Gestisci Esercizi del Paziente")
        
        esercizi_window = ttk.Frame(profilo_paziente_window, width=900, height=700)
        esercizi_window.pack_propagate(False)
        esercizi_window.pack(pady=20, padx=20)

        esercizi = self.controller.ottieni_esercizi_paziente(id_paziente)

        esercizi_listbox = tk.Listbox(esercizi_window, font=("Arial", 14), width=60, height=15)
        esercizi_listbox.pack(pady=10)
        
        if not esercizi:
            ttk.Label(esercizi_window, text="Nessun esercizio assegnato a questo paziente.", font=("Arial", 14)).pack(pady=10)
        else:
            for esercizio in esercizi:
                id_esercizio = esercizio[0]
                titolo = esercizio[1]
                descrizione = esercizio[2]
                esercizi_listbox.insert(tk.END, f"{id_esercizio}: {titolo} - {descrizione}")  
        
        stato_esercizio = ttk.Label(esercizi_window, text="", font=("Arial", 14), cursor="hand2")
        stato_esercizio.pack(pady=10)

        ttk.Button(esercizi_window, text="Aggiungi Esercizio",
                command=lambda: self.aggiungi_esercizio_al_paziente(id_paziente),
                style="TButton").pack(pady=10, ipadx=10, ipady=5)

        rimuovi_button = ttk.Button(esercizi_window, text="Rimuovi Esercizio",
                                    command=lambda: self.rimuovi_esercizio_al_paziente(id_paziente, esercizi_listbox, profilo_paziente_window),
                                    style="TButton")
        rimuovi_button.pack(pady=10, ipadx=10, ipady=5)

        def mostra_video_caricato(event):
            selezione = esercizi_listbox.curselection()
            if selezione:
                indice = selezione[0]
                esercizio_selezionato = esercizi_listbox.get(indice)
                id_esercizio = int(esercizio_selezionato.split(":")[0])
                
                """                
                percorso_video = self.controller.ottieni_url_video_paziente(id_paziente, id_esercizio)
                
              
                if percorso_video:
                    video_paziente.config(text=f"Video Caricato: {percorso_video}", foreground="blue", cursor="hand2")
                    video_paziente.bind("<Button-1>", lambda e: self.apri_url(percorso_video))
                else:
                    video_paziente.config(text="Il paziente non ha caricato nessun video per questo esercizio.", foreground="blue", cursor="hand2")
                """

                if self.controller.db.ottieni_stato_esercizio(id_paziente, id_esercizio) == 'completato':
                    stato_esercizio.config(text="Il paziente ha completato l'esercizio", cursor="hand2", foreground="green")
                else:
                    stato_esercizio.config(text="Il paziente NON ha ancora completato l'esercizio", cursor="hand2", foreground="red")

        esercizi_listbox.bind("<<ListboxSelect>>", mostra_video_caricato)







    def rimuovi_esercizio_al_paziente(self, id_paziente, listbox, profilo_paziente_window):
        selezione = listbox.curselection()

        if selezione:
            indice = selezione[0]
            esercizio_selezionato = listbox.get(indice)
            
            id_esercizio = int(esercizio_selezionato.split(":")[0])
            titolo_esercizio = esercizio_selezionato.split(":")[1].strip()  

            # Conferma la rimozione con un messaggio di conferma
            conferma = messagebox.askyesno("Conferma", f"Sei sicuro di voler rimuovere l'esercizio '{titolo_esercizio}'?")

            if conferma:
                
                self.controller.rimuovi_esercizio_paziente(id_esercizio, id_paziente)

                listbox.delete(indice)
                profilo_paziente_window.destroy()

                messagebox.showinfo("Successo", "L'esercizio è stato rimosso con successo.")
        else:
            messagebox.showerror("Errore", "Seleziona un esercizio da rimuovere.")

    
    

    def aggiungi_esercizio_al_paziente(self, id_paziente):
        aggiungi_window = tk.Toplevel(self.root)
        aggiungi_window.title("Aggiungi Esercizio al Paziente")
        
        aggiungi_frame = ttk.Frame(aggiungi_window, width=900, height=700)
        aggiungi_frame.pack_propagate(False)
        aggiungi_frame.pack(pady=20, padx=20)
        
        label = tk.Label(aggiungi_frame, text = "Clicca l'esercizio da assegnare al paziente:", font = ("Arial",16, "bold"))
        label.pack(pady=10)

        esercizi_assegnati = self.controller.ottieni_esercizi_paziente(id_paziente)
        
        id_esercizi_assegnati = [esercizio[0] for esercizio in esercizi_assegnati]
        
        esercizi_predefiniti = self.controller.ottieni_esercizi()
        
        esercizi_disponibili = [esercizio for esercizio in esercizi_predefiniti if esercizio[0] not in id_esercizi_assegnati]
        
        listbox_esercizi = tk.Listbox(aggiungi_frame, font=("Arial", 14), width=70, height=15)
        listbox_esercizi.pack(pady=10)

        for esercizio in esercizi_disponibili:
            listbox_esercizi.insert(tk.END, f"{esercizio[1]}: {esercizio[2]}")  

        def on_double_click(event):
            selezione = listbox_esercizi.curselection()
            if selezione:
                index = selezione[0]
                esercizio_selezionato = esercizi_disponibili[index]
                id_esercizio = esercizio_selezionato[0]
                
                self.controller.aggiungi_esercizio_paziente(id_paziente, id_esercizio)
                self.controller.ottieni_esercizi()
                
                messagebox.showinfo("Successo", f"Esercizio '{esercizio_selezionato[1]}' assegnato con successo.")
                aggiungi_window.destroy()

        listbox_esercizi.bind("<Double-1>", on_double_click)


    


        
# ----------------------------------------------------- GESTIONE LISTA ESERCIZI -------------------------------------


    



    
    def mostra_form_aggiungi_esercizio(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Aggiungi nuovo Esercizio")
        
        self.main_frame = tk.Frame(form_window, width=900, height=700)
        self.main_frame.pack_propagate(False)  
        self.main_frame.pack(pady=10)
        
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12, "bold"))
        
        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
        ttk.Label(self.main_frame, text="Titolo Esercizio", font=("Arial", 12)).pack(pady=5)
        titolo_entry = ttk.Entry(self.main_frame, font=("Arial", 12), width=40)
        titolo_entry.pack(pady=10)
        
        
        ttk.Label(self.main_frame, text="Descrizione", font=("Arial", 12)).pack(pady=5)
        descrizione_entry = tk.Text(self.main_frame, height=5, width=40)  
        descrizione_entry.pack(pady=10)
        
        self.upload_button = ttk.Button(self.main_frame, text="Carica un Video", command=self.carica_file_video)
        self.upload_button.pack(pady=20, ipadx=10, ipady=5)

        self.file_label = ttk.Label(self.main_frame, text="Nessun file selezionato", font=("Arial", 12)).pack(pady=5)
        
        submit_button = ttk.Button(self.main_frame, text="Aggiungi Esercizio", 
                                  command=lambda: self.aggiungi_esercizio(titolo_entry.get(), 
                                                                          descrizione_entry.get("1.0", "end-1c"), 
                                                                          self.file_video_path, form_window))
        submit_button.pack(pady=20, ipadx=10, ipady=5)
        
        back_button = ttk.Button(self.main_frame, text="Torna Indietro", command=form_window.destroy)
        back_button.pack(pady=20, ipadx=10, ipady=5)
        
        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)
        
        
    def aggiungi_esercizio (self, titolo, descrizione, video_url, window):
        if titolo and descrizione:
            video_url = ""
        self.controller.aggiungi_nuovo_esercizio(titolo, descrizione, video_url)        
        window.destroy()

        
        
    def mostra_lista_esercizi(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Lista degli esercizi")

        self.main_frame = tk.Frame(form_window, width=900, height=800)
        self.main_frame.pack_propagate(False)  
        self.main_frame.pack()

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12, "bold"))

        self.spazio = ttk.Label(self.main_frame)
        self.spazio.pack(expand=True)

        
        esercizi = self.controller.ottieni_esercizi() 

      
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(pady=10)

        self.search_entry = ttk.Entry(self.search_frame,font=("Arial", 14), width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=10)
 
        self.search_entry.bind("<KeyRelease>", self.cerca_esercizi)

        self.listbox = tk.Listbox(self.main_frame, width=80, height=15, font=("Arial", 14))
        self.listbox.pack(padx=10, pady=10)

       
        if not esercizi:
            ttk.Label(self.main_frame, text="Nessun esercizio trovato.").pack()
        else:
            self.esercizi_data = {}  
            
            for esercizio in esercizi:
                id_esercizio = esercizio[0]  
                titolo = esercizio[1]
                descrizione = esercizio[2]

          
                self.listbox.insert(tk.END, f"{id_esercizio}: {titolo}")
                # Memorizza le informazioni degli esercizi nel dizionario
                self.esercizi_data[id_esercizio] = {
                    "titolo": titolo,
                    "descrizione": descrizione,
                    "video_url": esercizio[3]  
                }

        self.listbox.bind("<Double-1>", lambda event: self.mostra_dettagli_esercizio(self.listbox, self.esercizi_data, event))

        back_button = ttk.Button(self.main_frame, text="Torna Indietro", command=form_window.destroy)
        back_button.pack(pady=20, ipadx=10, ipady=5)

        aggiungi_button = ttk.Button(self.main_frame, text="Aggiungi Esercizio", command=self.mostra_form_aggiungi_esercizio)
        aggiungi_button.pack(pady=20, ipadx=10, ipady=5)

        remove_button = ttk.Button(self.main_frame, text="Rimuovi Esercizio", command=lambda:self.rimuovi_esercizio_lista(self.listbox))
        remove_button.pack(pady=20, ipadx=10, ipady=5)

        self.spazio2 = ttk.Label(self.main_frame)
        self.spazio2.pack(expand=True)

    def cerca_esercizi(self, event=None):
        
        search_text = self.search_entry.get().lower()
        
        self.listbox.delete(0, tk.END)
        
        for id_esercizio, info in self.esercizi_data.items():
            if search_text in info['titolo'].lower():  
                self.listbox.insert(tk.END, f"{id_esercizio}: {info['titolo']}")



        
    def carica_file_video(self):
        file_path = simpledialog.askstring("Carica Video", "Inserisci l'URL del video:")
        if file_path:
            self.file_video_path = file_path  
            self.file_label.config(text=f"Video selezionato: {file_path.split('/')[-1]}")
            
    def rimuovi_esercizio_lista(self, listbox):
        selezione = self.listbox.curselection()
        if selezione:
            indice = selezione[0]
            esercizio = listbox.get(indice)
            id_esercizio= int(esercizio.split(":")[0])
            titolo_esercizio = esercizio.split(":")[1].strip() 

            
            conferma = messagebox.askyesno("Conferma", f"Sei sicuro di voler eliminare l'esercizio '{titolo_esercizio}'?")
            if conferma:
                self.controller.elimina_esercizio(id_esercizio)

                self.listbox.delete(indice)
        else:
            messagebox.showerror("Errore", "Seleziona un esercizio da eliminare.")
            
            
    def mostra_dettagli_esercizio(self, listbox, esercizi_data, event):
        try:
            selezione = listbox.curselection()  
            if selezione:
                indice = selezione[0]  
                esercizio_selezionato = listbox.get(indice) 
                
                id_esercizio = int(esercizio_selezionato.split(":")[0])

                dettagli_esercizio = esercizi_data[id_esercizio]

                self.visualizza_dettagli_esercizio(dettagli_esercizio, id_esercizio)
        except Exception as e:
            print(f"Errore durante la visualizzazione dei dettagli dell'esercizio: {e}")



    def visualizza_dettagli_esercizio(self, dettagli, id_esercizio):
        
        
        dettagli_window = tk.Toplevel(self.root)
        dettagli_window.title(f"Dettagli Esercizio: {dettagli['titolo']}")
        dettagli_window.geometry("1000x800")  

        titolo_font = font.Font(family="Arial", size=14, weight="bold")
        testo_font = font.Font(family="Arial", size=14)

        titolo_label = tk.Label(dettagli_window, text="Titolo:", font=titolo_font, bg="#f0f0f0")
        titolo_label.pack(pady=10)
        titolo_entry = tk.Entry(dettagli_window, font=testo_font, width=60)
        titolo_entry.insert(0, dettagli['titolo'])
        titolo_entry.pack(pady=10)

        descrizione_label = tk.Label(dettagli_window, text="Descrizione:", font=titolo_font, bg="#f0f0f0")
        descrizione_label.pack(pady=10)

        descrizione_text = tk.Text(dettagli_window,height=15, width=80, font=testo_font, bg="#ffffff", fg="#333333")
        descrizione_text.pack(pady=10)
        descrizione_text.insert(tk.END, dettagli['descrizione'])
        
        video_url_label = tk.Label(dettagli_window, fg="blue", cursor="hand2")
        video_url_label.pack(pady=10)
    
        # Mostra l'URL del video se disponibile
        if dettagli['video_url']:
            video_url_label.config(text=f"Video URL: {dettagli['video_url']}")
            video_url_label.bind("<Button-1>", lambda e: self.apri_url(dettagli['video_url']))
        
        def carica_video():
            video_dialog = tk.Toplevel(dettagli_window)
            video_dialog.title("Inserisci URL Video")
            video_dialog.geometry("500x300")

            dialog_label = tk.Label(video_dialog, text="Inserisci l'URL del video:", font=testo_font)
            dialog_label.pack(pady=10)

            video_url_entry = tk.Entry(video_dialog, font=testo_font, width=60)
            video_url_entry.pack(pady=10)

            def conferma_url():
                nuovo_video_url = video_url_entry.get()
                self.file_video_path = nuovo_video_url
                if nuovo_video_url:
                    video_url_label.config(text=f"Video URL: {nuovo_video_url}")
                    video_url_label.bind("<Button-1>", lambda e: self.apri_url(nuovo_video_url))
                    carica_video_button.pack_forget()  
                    video_dialog.destroy()
        
            conferma_button = tk.Button(video_dialog, text="Conferma", command=conferma_url, bg="#2196F3", fg="white", font=testo_font)
            conferma_button.pack(pady=10)

        carica_video_button = tk.Button(dettagli_window, text="Carica Video", command=carica_video, bg="#2196F3", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        carica_video_button.pack(pady=10)
        
        def salva_modifiche():
            nuovo_titolo = titolo_entry.get()
            nuova_descrizione = descrizione_text.get("1.0", tk.END).strip()  

            if nuovo_titolo != dettagli['titolo'] or nuova_descrizione != dettagli['descrizione'] or self.file_video_path != dettagli['video_url']:
                self.controller.modifica_esercizio(nuovo_titolo, nuova_descrizione, id_esercizio, self.file_video_path)
                dettagli_window.destroy() 
            else:
                messagebox.showerror("Nessuna modifica da salvare.")

        salva_button = tk.Button(dettagli_window, text="Salva Modifiche", command=salva_modifiche,
                                bg="#4CAF50", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        salva_button.pack(pady=20)

        back_button = tk.Button(dettagli_window, text="Torna Indietro", command=dettagli_window.destroy,
                                bg="#f44336", fg="white", font=testo_font, bd=0, relief="flat", padx=20, pady=10)
        back_button.pack(pady=10)

    def apri_url(self, url):
        import webbrowser
        webbrowser.open(url)

            

            
            
            
    # ------------------------------------------------ SEZIONE MEXAGGI -------------------------------
        

    def apri_chat_paziente(self, event):

        selezione = self.results_listbox.curselection()
        if selezione:
            indice = selezione[0]
            paziente = self.controller.pazienti[indice]
            root = tk.Tk() 
            self.messaggi = MessaggiView(root, paziente['id'], 1, 1)

        

    
    

    

            
            
            
            
            
    #-------------------------------------------              PRENOTAZIONI         ----------------------------------------        
    
            
    def mostra_prenotazioni(self):
        prenotazioni_window = tk.Toplevel(self.root)
        prenotazioni_window.title("Gestisci Prenotazioni")
        prenotazioni_window.geometry("900x700")  
        prenotazioni_window.config(bg="#f5f5f5")  

        title_label = tk.Label(prenotazioni_window, text="Elenco Prenotazioni", font=("Arial", 16, "bold"), bg="#f5f5f5")
        title_label.pack(pady=10)

        frame = tk.Frame(prenotazioni_window)
        frame.pack(pady=10)

        self.results_listbox = tk.Listbox(frame, width=70, height=20, font=("Arial", 14), bg="#ffffff", selectbackground="#cceeff")
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.results_listbox.yview)

        prenotazioni = self.prenotazione_controller.visualizza_prenotazioni_fisioterapista()

        self.results_listbox.delete(0, tk.END)

        if not prenotazioni:
            messagebox.showinfo("Nessuna Prenotazione", "Non ci sono prenotazioni disponibili.")
        else:
            for prenotazione in prenotazioni:
                # prenotazione[0] = ID prenotazione
                # prenotazione[1] = Nome paziente
                # prenotazione[2] = Data della prenotazione
                self.results_listbox.insert(
                    tk.END, 
                    f"ID-prenotazione: {prenotazione[0]}, Paziente: {prenotazione[1]}, Data: {prenotazione[2]}"
                )
        
        remove_button = ttk.Button(prenotazioni_window, text="Rimuovi Prenotazione", command=self.rimuovi_prenotazione)
        remove_button.pack(pady=10)
        
        back_button = ttk.Button(prenotazioni_window, text="Torna Indietro", command=prenotazioni_window.destroy, style="TButton")
        back_button.pack(pady=20, ipadx=10, ipady=5)

        remove_button.config(width=20)
        
    def rimuovi_prenotazione(self):
        selezione = self.results_listbox.curselection()
        if selezione:
            indice = selezione[0]
            prenotazione_selezionata = self.results_listbox.get(indice)
            id_prenotazione = int(prenotazione_selezionata.split(",")[0].split(":")[1].strip())

            self.prenotazione_controller.rimuovi_prenotazione(id_prenotazione)

            self.results_listbox.delete(indice)

            messagebox.showinfo("Successo", "Prenotazione rimossa con successo.")
        else:
            messagebox.showerror("Errore", "Seleziona una prenotazione da rimuovere.")
  
                     
#Label: Visualizza del testo o immagini statiche.
#Entry: Campo di input per una singola riga di testo.
#Button: Crea un pulsante per eseguire azioni.
#Frame: Contenitore per organizzare altri widget.
#Toplevel: Crea finestre indipendenti.
#Text: Campo per testo multilinea.
#Listbox: Lista di elementi selezionabili