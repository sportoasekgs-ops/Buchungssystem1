# Production Deployment Checkliste - SportOase

## Status: VORBEREITET - Warte auf IServ-Konfiguration

---

## ✅ ERLEDIGT

### Sicherheit & Konfiguration
- [x] SESSION_SECRET wird streng erzwungen (keine Fallback-Werte)
- [x] Keine sensiblen Daten in Logs (DATABASE_URL entfernt)
- [x] IServ SSO Integration implementiert (OAuth2/OpenID Connect)
- [x] CSRF-Protection auf allen POST-Routes
- [x] Render Production Database konfiguriert (DATABASE_URL in Production-Env gesetzt)

### Datenbank
- [x] User-Model erweitert für OAuth (oauth_provider, oauth_id, nullable password)
- [x] Migration für OAuth-Felder vorhanden (migration_add_oauth_fields.py)
- [x] Dual-Login unterstützt (Passwort + IServ SSO)

### Code-Qualität
- [x] Architect Review durchgeführt - APPROVED
- [x] Keine Mock-Daten im Code
- [x] Saubere Fehlerbehandlung

---

## ⏳ NÄCHSTE SCHRITTE - PRODUCTION READY MACHEN

### 1. IServ-Integration aktivieren (BLOCKIERT - braucht Admin)

**Was fehlt:**
```bash
# Diese 3 Umgebungsvariablen müssen in Replit Secrets gesetzt werden:
ISERV_BASE_URL=https://kgs-pattensen.de  # IServ-Server-URL
ISERV_CLIENT_ID=<vom IServ-Admin>        # OAuth Client-ID
ISERV_CLIENT_SECRET=<vom IServ-Admin>    # OAuth Client-Secret
```

**Wo bekommt man das:**
- IServ-Administrator muss im IServ-Panel konfigurieren:
  - Pfad: `Verwaltung → System → Single-Sign-On`
  - Neue OAuth2-App erstellen
  - Redirect URI: `https://sportoase.app/oauth/callback`
  - Scopes: `openid profile email`

**Was passiert danach:**
- Button "Mit IServ anmelden" erscheint auf Login-Seite
- IServ-User können sich direkt mit Schul-Zugangsdaten anmelden
- Rolle wird automatisch zugewiesen:
  - morelli.maurizio@kgs-pattensen.de → Admin
  - Alle anderen IServ-User → Lehrer

---

### 2. Production-Datenbank Migration durchführen

**Aktueller Stand:**
- Production DATABASE_URL ist gesetzt ✓
- Migration-Script existiert (migration_add_oauth_fields.py) ✓

**Was zu tun ist:**
```bash
# WICHTIG: VOR dem Render-Deployment ausführen!
# Option A: Migration direkt auf Render-DB laufen lassen
python3 migration_add_oauth_fields.py

# Option B: Falls existierende Production-DB vorhanden
# 1. Backup der Production-DB erstellen
# 2. Migration testen
# 3. Bei Erfolg: Live schalten
```

**Was die Migration macht:**
- Fügt `oauth_provider` (VARCHAR 50) zu User-Tabelle hinzu
- Fügt `oauth_id` (VARCHAR 255) zu User-Tabelle hinzu
- Macht `password_hash` nullable (für OAuth-only User)
- Erstellt unique constraint auf (oauth_provider, oauth_id)

---

### 3. SMTP/Email-Konfiguration überprüfen

**Aktueller Stand:**
- Gmail-Integration ist als Connector vorhanden (needs setup)
- SMTP-Variablen für Fallback sollten gesetzt sein

**Was zu tun ist:**
```bash
# Diese Variablen sollten in Production gesetzt sein:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=sportoase.kg@gmail.com
SMTP_PASS=<App-Passwort>
SMTP_FROM=sportoase.kg@gmail.com
ADMIN_EMAIL=sportoase.kg@gmail.com
```

**ODER:** Gmail-Connector richtig konfigurieren (bevorzugt)

---

### 4. Render Deployment vorbereiten

**Was zu überprüfen:**
- [ ] Alle Environment Variables in Render gesetzt:
  - SESSION_SECRET (neuen zufälligen Wert generieren!)
  - DATABASE_URL (bereits gesetzt ✓)
  - ISERV_BASE_URL
  - ISERV_CLIENT_ID
  - ISERV_CLIENT_SECRET
  - SMTP_* Variablen

- [ ] Render Build-Settings:
  ```
  Build Command: pip install -r requirements.txt
  Start Command: gunicorn --bind 0.0.0.0:$PORT --reuse-port main:app
  ```

- [ ] Python Version: 3.11

---

### 5. Nach Deployment: Testing

**Test-Checkliste:**
- [ ] Normale Login funktioniert (Passwort)
- [ ] IServ SSO Login funktioniert
- [ ] Admin-User (morelli.maurizio@kgs-pattensen.de) hat Admin-Rechte
- [ ] Andere IServ-User haben Lehrer-Rechte
- [ ] Buchungen können erstellt werden
- [ ] Email-Benachrichtigungen funktionieren
- [ ] Dashboard lädt korrekt
- [ ] Keine Fehler in Production-Logs

---

## 📝 Wichtige Notizen

### Sicherheit
- **SESSION_SECRET**: NIEMALS den Replit-Wert in Production verwenden! Neuen generieren.
- **Database Credentials**: Bereits sicher (nicht in Logs)
- **OAuth Secrets**: Werden vom IServ-Admin bereitgestellt

### Rollback-Plan
Falls nach Deployment Probleme auftreten:
1. IServ-Button kann durch Entfernen der ISERV_* Variablen deaktiviert werden
2. Traditioneller Login bleibt immer funktionsfähig
3. Database-Backup vor Migration erstellen!

### Support-Kontakte
- IServ-Administrator: [Name eintragen]
- Render Support: https://render.com/support
- Gmail API: Google Workspace Admin

---

## 🎯 Deployment-Reihenfolge (WICHTIG!)

```
1. IServ-Admin kontaktieren → Client-ID/Secret erhalten
   ↓
2. Environment Variables in Render setzen (inkl. neues SESSION_SECRET!)
   ↓
3. Database-Backup erstellen
   ↓
4. Migration auf Production-DB ausführen
   ↓
5. App auf Render deployen
   ↓
6. Testing durchführen (siehe Checkliste oben)
   ↓
7. Bei Erfolg: User informieren, dass IServ-Login verfügbar ist
```

---

**Zuletzt aktualisiert:** 24. November 2025
**Version:** 1.0 - IServ SSO Integration abgeschlossen
