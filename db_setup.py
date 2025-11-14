# Skript zur Initialisierung der PostgreSQL-Datenbank
# Dieses Skript erstellt die Datenbank und legt einen Admin-Benutzer an

import os
from app import app
from models import db, create_user, get_user_by_username

def setup_database():
    """Initialisiert die Datenbank und erstellt einen Standard-Admin-Account"""
    with app.app_context():
        print("Initialisiere Datenbank...")
        db.create_all()
        
        # Prüfe, ob bereits ein Admin existiert
        admin = get_user_by_username('sportoase')
        if not admin:
            # Erstelle Standard-Admin
            admin_id = create_user('sportoase', 'mauro123', 'admin', 'sportoase@sportoase.de')
            if admin_id:
                print(f"Admin-Account erstellt:")
                print(f"  Benutzername: sportoase")
                print(f"  Passwort: mauro123")
            else:
                print("Admin-Account konnte nicht erstellt werden.")
        else:
            print("Admin-Account existiert bereits.")
        
        print("\nDatenbank-Setup abgeschlossen!")
        print("Sie können sich jetzt mit den Admin-Zugangsdaten anmelden.")

if __name__ == '__main__':
    setup_database()
