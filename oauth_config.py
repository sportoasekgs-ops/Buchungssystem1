# IServ OAuth2/OpenID Connect Konfiguration für SportOase
# Diese Datei konfiguriert die SSO-Integration mit IServ

import os
from authlib.integrations.flask_client import OAuth

def init_oauth(app):
    """Initialisiert OAuth2 mit IServ-Konfiguration"""
    oauth = OAuth(app)
    
    # IServ-Instanz-Domain aus Umgebungsvariablen
    iserv_domain = os.environ.get('ISERV_DOMAIN', 'kgs-pattensen.de')
    iserv_base_url = f'https://{iserv_domain}'
    
    # Registriere IServ als OAuth-Provider
    # NUR grundlegende Scopes - keine groups/roles da IServ diese evtl. nicht erlaubt
    iserv = oauth.register(
        name='iserv',
        client_id=os.environ.get('ISERV_CLIENT_ID'),
        client_secret=os.environ.get('ISERV_CLIENT_SECRET'),
        server_metadata_url=f'{iserv_base_url}/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid profile email'
        }
    )
    
    return oauth, iserv

def get_admin_email():
    """Gibt die E-Mail-Adresse des Admin-Benutzers zurück"""
    return 'morelli.maurizio@kgs-pattensen.de'

def is_admin_email(email):
    """Prüft, ob die E-Mail-Adresse dem Admin gehört"""
    return email and email.lower().strip() == get_admin_email().lower()

def determine_user_role(userinfo):
    """
    Bestimmt die Rolle des Benutzers - VEREINFACHT ohne Gruppen-Scope
    
    Regelwerk (IServ kontrolliert Zugang über OAuth-App-Berechtigungen):
    - morelli.maurizio@kgs-pattensen.de → admin
    - Alle anderen mit @kgs-pattensen.de → teacher
    
    Args:
        userinfo: Dictionary mit Benutzerdaten von IServ
    
    Returns:
        'admin', 'teacher' oder None (kein Zugang)
    """
    email = userinfo.get('email', '').lower().strip()
    
    # Log für Debugging
    print(f"🔍 Bestimme Rolle für: {email}")
    print(f"   UserInfo: {userinfo}")
    
    # 1. Admin-E-Mail hat immer Admin-Zugang
    if is_admin_email(email):
        print(f"   → Admin (morelli.maurizio@kgs-pattensen.de)")
        return 'admin'
    
    # 2. Alle mit @kgs-pattensen.de E-Mail bekommen Lehrer-Berechtigung
    # (Schüler-Filterung erfolgt in IServ über OAuth-App-Gruppeneinschränkungen)
    if email.endswith('@kgs-pattensen.de'):
        print(f"   → Teacher (kgs-pattensen.de E-Mail)")
        return 'teacher'
    
    # Keine gültige Schul-E-Mail
    print(f"   → KEIN ZUGANG (keine @kgs-pattensen.de E-Mail)")
    return None


def extract_all_text(data):
    """
    Extrahiert ALLE Textwerte aus beliebigen Datenstrukturen.
    Rekursiv für verschachtelte Strukturen.
    """
    texts = []
    
    if isinstance(data, str):
        texts.append(data)
    elif isinstance(data, list):
        for item in data:
            texts.extend(extract_all_text(item))
    elif isinstance(data, dict):
        # Extrahiere alle String-Werte aus dem Dictionary
        for key, value in data.items():
            # Key selbst könnte relevant sein (z.B. Gruppenname als Key)
            if isinstance(key, str):
                texts.append(key)
            # Wert rekursiv extrahieren
            texts.extend(extract_all_text(value))
    
    return texts


def extract_names(data):
    """Extrahiert Namen aus verschiedenen Datenformaten"""
    names = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Format: [{name: "...", displayName: "...", id: "..."}]
                if 'name' in item:
                    names.append(item['name'])
                if 'Name' in item:
                    names.append(item['Name'])
                if 'displayName' in item:
                    names.append(item['displayName'])
            elif isinstance(item, str):
                names.append(item)
    elif isinstance(data, str):
        names.append(data)
    elif isinstance(data, dict):
        # IServ-Format: {'2124': {'id': 2124, 'name': 'Lehrer'}, ...}
        # Durchlaufe alle Werte im Dictionary
        for key, value in data.items():
            if isinstance(value, dict):
                if 'name' in value:
                    names.append(value['name'])
                if 'Name' in value:
                    names.append(value['Name'])
                if 'displayName' in value:
                    names.append(value['displayName'])
            elif isinstance(value, str):
                names.append(value)
        # Falls 'name' oder 'displayName' direkt im Dict ist
        if 'name' in data:
            names.append(data['name'])
        if 'displayName' in data:
            names.append(data['displayName'])
    return names
