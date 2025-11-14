# SportOase Buchungssystem

Eine Web-Anwendung zur Verwaltung von Buchungen für die Schul-SportOase mit Login-System und E-Mail-Benachrichtigungen.

## Funktionen

- **Benutzer-Authentifizierung**: Login-System für Lehrkräfte und Admins
- **Wochenplan-Anzeige**: Übersicht über feste und freie Zeitslots
- **Buchungssystem**: Lehrkräfte können 1-5 Schüler für Zeitslots anmelden
- **Kapazitätskontrolle**: Maximal 5 Schüler pro Zeitslot
- **Vorlaufzeit**: Buchungen nur bis 60 Minuten vor Stundenbeginn möglich
- **E-Mail-Benachrichtigungen**: Automatische Benachrichtigung bei neuen Buchungen
- **Admin-Panel**: Verwaltung von Lehrkräften und Übersicht aller Buchungen

## Installation auf Replit

### 1. Projekt starten

Das Projekt verwendet Python 3.11 und Flask. Die Abhängigkeiten werden automatisch installiert.

### 2. Datenbank initialisieren

Vor der ersten Nutzung muss die Datenbank initialisiert werden:

```bash
python db_setup.py
```

Dies erstellt:
- Die SQLite-Datenbank `sportoase.db`
- Einen Standard-Admin-Account:
  - **E-Mail**: admin@sportoase.de
  - **Passwort**: admin123

**WICHTIG**: Ändern Sie das Admin-Passwort nach dem ersten Login!

### 3. Anwendung starten

```bash
python app.py
```

Die Anwendung läuft dann auf Port 5000 und ist über den Replit-Webview erreichbar.

## Umgebungsvariablen (Optional)

Für E-Mail-Benachrichtigungen können folgende Umgebungsvariablen in Replit konfiguriert werden:

- `SMTP_HOST`: SMTP-Server-Adresse (z.B. smtp.gmail.com)
- `SMTP_PORT`: SMTP-Port (Standard: 587)
- `SMTP_USER`: SMTP-Benutzername
- `SMTP_PASS`: SMTP-Passwort
- `SMTP_FROM`: Absender-E-Mail-Adresse
- `ADMIN_EMAIL`: E-Mail-Adresse für Benachrichtigungen

Ohne SMTP-Konfiguration werden Benachrichtigungen nur in der Konsole ausgegeben.

## Projektstruktur

```
.
├── app.py                  # Haupt-Anwendung mit allen Routen
├── config.py               # Konfiguration (Stundenplan, SMTP, etc.)
├── models.py               # Datenbank-Modelle und Funktionen
├── db_setup.py             # Datenbank-Initialisierung
├── email_service.py        # E-Mail-Versand
├── templates/              # HTML-Templates
│   ├── base.html          # Basis-Template
│   ├── login.html         # Login-Seite
│   ├── dashboard.html     # Hauptseite mit Wochenplan
│   ├── book.html          # Buchungsformular
│   └── admin.html         # Admin-Bereich
├── static/                 # Statische Dateien
│   └── style.css          # CSS-Stylesheet
└── README.md              # Diese Datei
```

## Nutzung

### Als Admin

1. Login mit Admin-Zugangsdaten
2. Navigieren zum Admin-Bereich
3. Neue Lehrkräfte anlegen
4. Alle Buchungen einsehen und filtern

### Als Lehrkraft

1. Login mit eigenen Zugangsdaten
2. Datum im Dashboard auswählen
3. Verfügbare Zeitslots mit "Buchen" öffnen
4. Anzahl Schüler auswählen (1-5)
5. Schülerdaten eingeben (Name und Klasse)
6. Bei freien Slots: Modul auswählen
7. Buchung abschließen

## Wochenplan-Struktur

Die SportOase läuft während der Unterrichtszeit (1.-6. Stunde):

- **1. Stunde**: 07:50 - 08:35
- **2. Stunde**: 08:35 - 09:20
- **3. Stunde**: 09:40 - 10:25
- **4. Stunde**: 10:25 - 11:20
- **5. Stunde**: 11:40 - 12:25
- **6. Stunde**: 12:25 - 13:10

### Feste Angebote

Die Konfiguration in `config.py` definiert feste Angebote pro Wochentag:

- **Montag**: Stunden 1, 3, 5 fest
- **Dienstag**: Alle Stunden frei
- **Mittwoch**: Stunden 1, 3, 5 fest
- **Donnerstag**: Stunden 2, 5 fest
- **Freitag**: Stunden 2, 4, 5 fest

Freie Stunden können mit folgenden Modulen gebucht werden:
- Aktivierung
- Regulation / Entspannung
- Konflikt-Reset
- Egal / flexibel

## Anpassungen

### Stundenplan ändern

In `config.py` können Sie anpassen:

- `PERIOD_TIMES`: Zeiten der Schulstunden
- `FIXED_OFFERS`: Feste Angebote pro Wochentag
- `FREE_MODULES`: Verfügbare Module für freie Stunden
- `MAX_STUDENTS_PER_PERIOD`: Maximale Schüleranzahl
- `BOOKING_ADVANCE_MINUTES`: Vorlaufzeit für Buchungen

### Datenbank zurücksetzen

Um die Datenbank komplett zurückzusetzen:

```bash
rm sportoase.db
python db_setup.py
```

## Technologie-Stack

- **Backend**: Python 3.11, Flask
- **Datenbank**: SQLite
- **Templates**: Jinja2
- **Styling**: Einfaches CSS (schwarz-weiß)
- **E-Mail**: SMTP (smtplib)
- **Zeitzone**: Europe/Berlin (pytz)

## Support

Bei Fragen oder Problemen wenden Sie sich an Ihren Administrator.
