# IServ SSO Integration - Setup-Anleitung für SportOase

Diese Anleitung beschreibt, wie Sie die SportOase-App mit IServ SSO (Single Sign-On) verbinden.

## Übersicht

Die SportOase-App unterstützt **OAuth2/OpenID Connect** für die Authentifizierung über IServ. Damit können sich Lehrkräfte mit ihrem IServ-Account anmelden, ohne ein separates Passwort für SportOase zu benötigen.

### Rollenverwaltung

- **Admin**: `morelli.maurizio@kgs-pattensen.de` erhält automatisch Admin-Rechte
- **Lehrer**: Alle anderen IServ-Benutzer erhalten normale Lehrkraft-Rechte (keine Admin-Funktionen)

## Schritt 1: IServ-Admin-Konfiguration

### 1.1 Neue OAuth-Anwendung registrieren

Der IServ-Administrator muss folgende Schritte durchführen:

1. In IServ einloggen als Administrator
2. Navigieren zu: **Verwaltung → System → Single-Sign-On**
3. Klicken auf **"Hinzufügen"**

### 1.2 Allgemeine Einstellungen

Folgende Daten eingeben:

| Feld | Wert |
|------|------|
| **Name** | SportOase Buchungssystem |
| **Beschreibung** | Buchungssystem für die SportOase-Anmeldungen |
| **Vertrauenswürdig** | ✅ Ja (Haken setzen) |

**Wichtig**: Nach dem Speichern werden automatisch generiert:
- **Client-ID** (z.B. `sportoase_1234567`)
- **Client-Secret** (z.B. `a1b2c3d4...xyz`)

➡️ **Diese Werte notieren und sicher aufbewahren!**

### 1.3 Redirect URIs konfigurieren

In der OAuth-Konfiguration unter "Anwendung" folgende Callback-URL eintragen:

**Für Replit:**
```
https://sportoase.app/oauth/callback
```

**Für andere Domains:**
```
https://IHR_DOMAIN/oauth/callback
```

### 1.4 Scopes

Standardmäßig benötigte Scopes (automatisch konfiguriert):
- `openid` - Grundlegende Authentifizierung
- `profile` - Name des Benutzers
- `email` - E-Mail-Adresse

### 1.5 Benutzerrechte

Sicherstellen, dass die gewünschten Benutzer/Gruppen die Berechtigung **"OAuth verwenden"** haben:

1. Navigieren zu: **Verwaltung → Benutzer**
2. Benutzer/Gruppe auswählen
3. Unter "Rechte" → **"OAuth verwenden"** aktivieren

## Schritt 2: SportOase-App Konfiguration (Replit)

### 2.1 Umgebungsvariablen setzen

In Replit → **Secrets** (Schloss-Symbol) folgende Werte hinzufügen:

| Secret-Name | Wert | Beschreibung |
|-------------|------|--------------|
| `ISERV_DOMAIN` | `kgs-pattensen.de` | IServ-Instanz-Domain (ohne https://) |
| `ISERV_CLIENT_ID` | `[Client-ID von IServ]` | Von IServ generierte Client-ID |
| `ISERV_CLIENT_SECRET` | `[Client-Secret von IServ]` | Von IServ generiertes Client-Secret |

### 2.2 Beispiel

```
ISERV_DOMAIN=kgs-pattensen.de
ISERV_CLIENT_ID=sportoase_abc123
ISERV_CLIENT_SECRET=xyz789...
```

### 2.3 Workflow neu starten

Nach dem Setzen der Secrets:
1. Workflow stoppen
2. Workflow neu starten
3. Login-Seite aufrufen

➡️ Der **"Mit IServ anmelden"** Button sollte jetzt sichtbar sein!

## Schritt 3: Testen

### 3.1 IServ-Login testen

1. Auf der SportOase Login-Seite auf **"Mit IServ anmelden"** klicken
2. Weiterleitung zu IServ → Anmeldung mit IServ-Benutzername und Passwort
3. Bestätigung der Datenweitergabe (beim ersten Login)
4. Automatische Weiterleitung zurück zu SportOase
5. ✅ Erfolgreich angemeldet!

### 3.2 Admin-Rechte prüfen

**Admin-Account** (`morelli.maurizio@kgs-pattensen.de`):
- ✅ Zugriff auf Admin-Bereich
- ✅ Kann Buchungen verwalten
- ✅ Kann Slots blockieren
- ✅ Kann Slot-Namen ändern
- ✅ Kann Passwort ändern

**Lehrer-Accounts** (alle anderen):
- ✅ Können buchen
- ✅ Können eigene Buchungen sehen
- ❌ **Kein** Zugriff auf Admin-Funktionen

## Technische Details

### OAuth-Endpunkte

IServ stellt folgende OAuth2/OIDC-Endpunkte bereit:

```
Discovery: https://kgs-pattensen.de/.well-known/openid-configuration
Authorization: https://kgs-pattensen.de/iserv/oauth/v2/auth
Token: https://kgs-pattensen.de/iserv/oauth/v2/token
UserInfo: https://kgs-pattensen.de/iserv/public/oauth/userinfo
```

### Datenfluss

1. Benutzer klickt auf "Mit IServ anmelden"
2. Weiterleitung zu IServ Authorization Endpoint
3. Benutzer meldet sich bei IServ an
4. IServ leitet zurück mit Authorization Code
5. SportOase tauscht Code gegen Access Token
6. SportOase ruft UserInfo-Endpoint auf
7. Benutzer wird in SportOase angelegt/aktualisiert
8. Session wird erstellt → Benutzer ist angemeldet

### Sicherheit

✅ **OAuth2 + OpenID Connect** (Standard-Protokoll für SSO)
✅ **HTTPS** erforderlich (automatisch in Replit)
✅ **State-Parameter** gegen CSRF-Angriffe
✅ **Client-Secret** wird sicher auf Server gespeichert (nie im Browser)
✅ **Automatische Token-Verwaltung** durch Authlib

## Fehlerbehebung

### "IServ-Login ist nicht konfiguriert"

➡️ Prüfen Sie, ob `ISERV_CLIENT_ID` und `ISERV_CLIENT_SECRET` in Replit Secrets gesetzt sind

### "Fehler beim IServ-Login"

➡️ Prüfen Sie:
1. Redirect URI in IServ korrekt eingetragen?
2. Client-ID und Client-Secret korrekt kopiert?
3. IServ-Domain korrekt (`kgs-pattensen.de` ohne `https://`)?

### Button "Mit IServ anmelden" nicht sichtbar

➡️ Secrets gesetzt und Workflow neu gestartet?

### Benutzer erhält keine Admin-Rechte

➡️ Ist die E-Mail-Adresse exakt `morelli.maurizio@kgs-pattensen.de`?

## Duales Login-System

Die SportOase-App unterstützt **beide** Login-Methoden gleichzeitig:

1. **Traditioneller Login** (Benutzername + Passwort)
   - Für bestehende Accounts
   - Für Notfälle, falls IServ nicht erreichbar ist

2. **IServ SSO Login**
   - Für alle IServ-Benutzer
   - Automatische Account-Erstellung
   - Keine separaten Passwörter notwendig

## Support

Bei Fragen oder Problemen:
- **IServ-Konfiguration**: Kontaktieren Sie Ihren IServ-Administrator
- **SportOase-App**: Kontaktieren Sie `sportoase.kg@gmail.com`

## Changelog

- **2025-11-24**: IServ SSO Integration implementiert
- Unterstützung für OAuth2/OpenID Connect
- Automatische Rollenzuweisung (Admin vs. Lehrer)
- Duales Login-System (traditionell + SSO)
