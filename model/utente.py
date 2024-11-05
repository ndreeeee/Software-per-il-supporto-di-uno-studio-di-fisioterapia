class Utente:
    def __init__(self, nome, email, password):
        self.nome = nome
        self.email = email
        self.password = password

class Fisioterapista(Utente):
    def __init__(self, nome, email, password):
        super().__init__(nome, email, password)
        self.lista_pazienti = []


        
class Paziente(Utente):
    def __init__(self, nome, email, password):
        super().__init__(nome, email, password)
        self.esercizi_assegnati = []
        

