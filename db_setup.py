# Skript zur Initialisierung der Datenbank
# Dieses Skript erstellt die Datenbank und legt einen Admin-Benutzer an

from models import init_db, create_user, get_user_by_email

def setup_database():
    """Initialisiert die Datenbank und erstellt einen Standard-Admin-Account"""
    print("Initialisiere Datenbank...")
    init_db()
    
    # Prüfe, ob bereits ein Admin existiert
    admin = get_user_by_email('admin@sportoase.de')
    if not admin:
        # Erstelle Standard-Admin
        admin_id = create_user('admin@sportoase.de', 'admin123', 'admin')
        if admin_id:
            print(f"Admin-Account erstellt:")
            print(f"  E-Mail: admin@sportoase.de")
            print(f"  Passwort: admin123")
            print(f"  WICHTIG: Bitte ändern Sie das Passwort nach dem ersten Login!")
        else:
            print("Admin-Account konnte nicht erstellt werden.")
    else:
        print("Admin-Account existiert bereits.")
    
    print("\nDatenbank-Setup abgeschlossen!")
    print("Sie können sich jetzt mit den Admin-Zugangsdaten anmelden.")

if __name__ == '__main__':
    setup_database()
