# Datenbank-Migration: Fügt OAuth-Felder zur users-Tabelle hinzu
# Führe dieses Skript einmalig aus, um die Datenbank zu aktualisieren

from app import app, db

def add_oauth_fields():
    """Fügt oauth_provider und oauth_id Felder zur users-Tabelle hinzu"""
    with app.app_context():
        try:
            # ALTER TABLE mit PostgreSQL
            db.session.execute(db.text('''
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS oauth_provider VARCHAR(50),
                ADD COLUMN IF NOT EXISTS oauth_id VARCHAR(200)
            '''))
            
            # Password_hash nullable machen
            db.session.execute(db.text('''
                ALTER TABLE users 
                ALTER COLUMN password_hash DROP NOT NULL
            '''))
            
            # Unique Constraint hinzufügen
            db.session.execute(db.text('''
                ALTER TABLE users 
                ADD CONSTRAINT unique_oauth_user 
                UNIQUE (oauth_provider, oauth_id)
            '''))
            
            # Index auf email hinzufügen falls noch nicht vorhanden
            db.session.execute(db.text('''
                CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)
            '''))
            
            db.session.commit()
            print("✅ OAuth-Felder erfolgreich zur users-Tabelle hinzugefügt!")
            print("   - oauth_provider VARCHAR(50)")
            print("   - oauth_id VARCHAR(200)")
            print("   - password_hash ist jetzt nullable")
            print("   - Unique Constraint auf (oauth_provider, oauth_id)")
            print("   - Index auf email-Feld")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Fehler bei der Migration: {e}")
            print("Hinweis: Wenn Felder bereits existieren, ist das normal.")

if __name__ == '__main__':
    print("Starte OAuth-Felder Migration...")
    add_oauth_fields()
