# IServ OAuth2/OpenID Connect Konfiguration für SportOase
# Diese Datei konfiguriert die SSO-Integration mit IServ
# Unterstützt sowohl ROLES als auch GROUPS für maximale Kompatibilität

import os
import json
from authlib.integrations.flask_client import OAuth


def init_oauth(app):
    """Initialisiert OAuth2 mit IServ-Konfiguration"""
    oauth = OAuth(app)

    # IServ-Instanz-Domain aus Umgebungsvariablen
    iserv_domain = os.environ.get('ISERV_DOMAIN', 'kgs-pattensen.de')
    iserv_base_url = f'https://{iserv_domain}'

    # Registriere IServ als OAuth-Provider
    # Scopes: openid, profile, email, roles UND groups für maximale Kompatibilität
    # IServ-Dokumentation: https://doku.iserv.de/manage/system/sso/
    iserv = oauth.register(
        name='iserv',
        client_id=os.environ.get('ISERV_CLIENT_ID'),
        client_secret=os.environ.get('ISERV_CLIENT_SECRET'),
        server_metadata_url=f'{iserv_base_url}/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email roles groups'})

    return oauth, iserv


def get_admin_email():
    """Gibt die E-Mail-Adresse des Admin-Benutzers zurück"""
    return 'morelli.maurizio@kgs-pattensen.de'


def is_admin_email(email):
    """Prüft, ob die E-Mail-Adresse dem Admin gehört"""
    return email and email.lower().strip() == get_admin_email().lower()


def extract_roles_from_userinfo(userinfo):
    """
    Extrahiert Rollennamen aus IServ userinfo.
    
    IServ-Format laut Dokumentation (Scope: roles):
    {
        "roles": [
            {"uuid": "...", "id": 123, "name": "Lehrer"},
            {"uuid": "...", "id": 456, "name": "Mitarbeiter"}
        ]
    }
    
    Gibt eine Liste von Rollennamen zurück (lowercase).
    """
    roles = []
    
    # IServ liefert Rollen im Feld "roles" als Liste von Objekten
    if 'roles' in userinfo:
        roles_data = userinfo['roles']
        print(f"   📋 Raw 'roles' data: {roles_data}")
        
        if isinstance(roles_data, list):
            for role_item in roles_data:
                if isinstance(role_item, dict):
                    # IServ-Format: {"uuid": "...", "id": 123, "name": "Lehrer"}
                    if 'name' in role_item and isinstance(role_item['name'], str):
                        roles.append(role_item['name'].lower().strip())
                        print(f"   ✓ Rolle extrahiert: {role_item['name']}")
                elif isinstance(role_item, str):
                    # Fallback: direkter String
                    roles.append(role_item.lower().strip())
                    print(f"   ✓ Rolle (String): {role_item}")
        elif isinstance(roles_data, str):
            # Falls roles ein einzelner String ist
            roles.append(roles_data.lower().strip())
            print(f"   ✓ Rolle (einzelner String): {roles_data}")
    else:
        print(f"   ⚠️ Kein 'roles' Feld in userinfo gefunden")
    
    # Entferne Duplikate und leere Strings
    return list(set(r for r in roles if r))


def extract_groups_from_userinfo(userinfo):
    """
    Extrahiert Gruppennamen aus IServ userinfo.
    
    IServ-Format laut Dokumentation (Scope: groups):
    {
        "groups": [
            {"id": 123, "uuid": "...", "act": "lehrer", "name": "Lehrer"},
            {"id": 456, "uuid": "...", "act": "mitarbeiter", "name": "Mitarbeiter"}
        ]
    }
    
    Gibt eine Liste von Gruppennamen zurück (lowercase).
    """
    groups = []
    
    if 'groups' in userinfo:
        groups_data = userinfo['groups']
        print(f"   📋 Raw 'groups' data: {groups_data}")
        
        if isinstance(groups_data, list):
            for group_item in groups_data:
                if isinstance(group_item, dict):
                    # IServ-Format: {"id": 123, "uuid": "...", "act": "lehrer", "name": "Lehrer"}
                    if 'name' in group_item and isinstance(group_item['name'], str):
                        groups.append(group_item['name'].lower().strip())
                        print(f"   ✓ Gruppe extrahiert (name): {group_item['name']}")
                    if 'act' in group_item and isinstance(group_item['act'], str):
                        groups.append(group_item['act'].lower().strip())
                        print(f"   ✓ Gruppe extrahiert (act): {group_item['act']}")
                elif isinstance(group_item, str):
                    groups.append(group_item.lower().strip())
                    print(f"   ✓ Gruppe (String): {group_item}")
        elif isinstance(groups_data, str):
            groups.append(groups_data.lower().strip())
            print(f"   ✓ Gruppe (einzelner String): {groups_data}")
    else:
        print(f"   ⚠️ Kein 'groups' Feld in userinfo gefunden")
    
    return list(set(g for g in groups if g))


def determine_user_role(userinfo):
    """
    Bestimmt die Rolle des Benutzers basierend auf IServ-ROLLEN und GRUPPEN.
    
    Regelwerk:
    1. Admin-E-Mail → admin (immer erlaubt)
    2. Rolle/Gruppe enthält "Lehrer", "Mitarbeiter", etc. → teacher
    3. Rolle/Gruppe enthält "Schüler" → KEIN ZUGANG
    4. Keine passende Rolle/Gruppe → KEIN ZUGANG
    
    Args:
        userinfo: Dictionary mit Benutzerdaten von IServ
    
    Returns:
        Tuple: (role, iserv_role) wobei:
        - role: 'admin', 'teacher' oder None (kein Zugang)
        - iserv_role: Die erkannte IServ-Rolle/Gruppe
    """
    email = userinfo.get('email', '').lower().strip()

    # === AUSFÜHRLICHES LOGGING ===
    print("=" * 70)
    print(f"🔐 IServ OAuth Login-Versuch")
    print(f"   E-Mail: {email}")
    print(f"   UserInfo Keys: {list(userinfo.keys())}")
    print("-" * 70)
    
    # Logge die komplette userinfo für Debugging
    print(f"   📋 Komplette UserInfo:")
    for key, value in userinfo.items():
        value_str = str(value)
        if len(value_str) > 300:
            value_str = value_str[:300] + "..."
        print(f"      {key}: {value_str}")
    
    print("-" * 70)
    
    # Extrahiere Rollen UND Gruppen
    roles = extract_roles_from_userinfo(userinfo)
    groups = extract_groups_from_userinfo(userinfo)
    
    # Kombiniere Rollen und Gruppen für die Prüfung
    all_memberships = roles + groups
    
    print("-" * 70)
    print(f"   🏷️ Extrahierte Rollen: {roles}")
    print(f"   👥 Extrahierte Gruppen: {groups}")
    print(f"   📊 Kombinierte Mitgliedschaften: {all_memberships}")
    print("=" * 70)

    # 1. Admin-E-Mail hat immer Admin-Zugang
    if is_admin_email(email):
        print(f"   ✅ Admin erkannt (E-Mail-Match: {get_admin_email()})")
        return 'admin', 'Administrator'

    # Prüfe E-Mail-Domain
    if not email.endswith('@kgs-pattensen.de'):
        print(f"   ❌ KEIN ZUGANG - Keine @kgs-pattensen.de E-Mail")
        return None, None

    # 2. Prüfe auf erlaubte Rollen/Gruppen
    # Diese Keywords geben Zugang (EINHEITLICHE RECHTE als 'teacher'):
    allowed_keywords = [
        # Schulleitung
        'schulleitung',
        # Lehrer
        'lehrer',
        'lehrerin',
        'teacher',
        # Sozialpädagogen
        'sozialpädagog',
        'sozialpaedagog',
        'sozialpädagogin',
        # Pädagogische Mitarbeiter
        'pädagogische mitarbeiter',
        'paedagogische mitarbeiter',
        'pädagogischer mitarbeiter',
        # Mitarbeiter (allgemein)
        'mitarbeiter',
        'mitarbeitende',
        'mitarbeiterin',
        # Sekretariat
        'sekretariat',
        'verwaltung',
    ]
    
    # Schüler werden blockiert
    blocked_keywords = [
        'schüler',
        'schueler',
        'schülerin',
        'schuelerin',
        'student',
        'students',
    ]
    
    # Zuerst prüfen ob blockierte Rolle/Gruppe vorhanden
    for membership in all_memberships:
        for blocked in blocked_keywords:
            if blocked in membership:
                print(f"   ❌ KEIN ZUGANG - Schüler-Rolle/Gruppe erkannt: '{membership}'")
                return None, None
    
    # Dann prüfen ob erlaubte Rolle/Gruppe vorhanden
    for membership in all_memberships:
        for allowed in allowed_keywords:
            if allowed in membership:
                # Formatiere für Anzeige
                display_role = membership.replace('_', ' ').title()
                print(f"   ✅ Zugang gewährt - Rolle/Gruppe erkannt: '{membership}' (matched '{allowed}')")
                return 'teacher', display_role
    
    # Keine passende Rolle/Gruppe gefunden
    if all_memberships:
        print(f"   ❌ KEIN ZUGANG - Keine erlaubte Rolle/Gruppe gefunden")
        print(f"   ℹ️ Gefundene Mitgliedschaften: {all_memberships}")
        print(f"   ℹ️ Erlaubte Keywords: {allowed_keywords[:5]}... (und weitere)")
    else:
        print(f"   ❌ KEIN ZUGANG - Keine Rollen/Gruppen in userinfo gefunden")
        print(f"   ⚠️ HINWEIS: Stellen Sie sicher, dass in IServ Admin → Single-Sign-On")
        print(f"      die Scopes 'roles' und/oder 'groups' für diese App aktiviert sind!")
    
    return None, None
