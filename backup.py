import os
import shutil
from datetime import datetime

def backup_database():
    db_file = "gestione_fisioterapia.db"  

    # Directory di backup
    backup_dir = r"C:\Users\andre\Desktop\BackupIngegneriadelSoftware"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Nome del file di backup con data
    data_corrente = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"{backup_dir}/backup_{data_corrente}.db"

    try:
        shutil.copy(db_file, backup_file)
        print(f"Backup eseguito con successo: {backup_file}")
        return 1
    except Exception as e:
        print(f"Errore durante il backup: {e}")
        return 0

if __name__ == "__main__":
    backup_database()
