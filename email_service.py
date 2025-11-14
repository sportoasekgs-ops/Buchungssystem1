# E-Mail-Service für Buchungsbenachrichtigungen
# Sendet E-Mails über SMTP an Admins und Lehrkräfte

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, ADMIN_EMAIL
import json

def send_booking_notification(booking_data, teacher_email):
    """
    Sendet eine E-Mail-Benachrichtigung über eine neue Buchung
    
    booking_data: Dictionary mit Buchungsinformationen
    teacher_email: E-Mail-Adresse der Lehrkraft
    """
    
    # Wenn SMTP nicht konfiguriert ist, Nachricht nur ausgeben
    if not SMTP_USER or not SMTP_PASS or SMTP_HOST == 'smtp.example.com':
        print("\n=== E-Mail-Benachrichtigung (SMTP nicht konfiguriert) ===")
        print(f"An: {ADMIN_EMAIL}")
        print(f"Betreff: Neue SportOase-Buchung für {booking_data['date']}")
        print(f"\nDatum: {booking_data['date']}")
        print(f"Stunde: {booking_data['period']}")
        print(f"Angebot: {booking_data['offer_label']} ({booking_data['offer_type']})")
        print(f"Lehrkraft: {booking_data.get('teacher_name', 'N/A')} (Klasse {booking_data.get('teacher_class', 'N/A')})")
        print(f"Schüler:")
        for student in booking_data['students']:
            print(f"  - {student['name']} (Klasse {student['klasse']})")
        print("=" * 50 + "\n")
        return True
    
    try:
        # E-Mail-Inhalt erstellen
        students_list = "\n".join([
            f"  - {s['name']} (Klasse {s['klasse']})" 
            for s in booking_data['students']
        ])
        
        subject = f"Neue SportOase-Buchung für {booking_data['date']}"
        body = f"""
Neue Buchung in der SportOase:

Datum: {booking_data['date']} ({booking_data['weekday']})
Stunde: {booking_data['period']}. Stunde
Angebot: {booking_data['offer_label']} ({booking_data['offer_type']})
Lehrkraft: {booking_data.get('teacher_name', 'N/A')} (Klasse {booking_data.get('teacher_class', 'N/A')})

Angemeldete Schüler:
{students_list}

Anzahl Schüler: {len(booking_data['students'])}

---
Diese E-Mail wurde automatisch vom SportOase-Buchungssystem generiert.
"""
        
        # E-Mail an Admin senden
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # SMTP-Verbindung aufbauen und E-Mail senden
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"E-Mail-Benachrichtigung an {ADMIN_EMAIL} gesendet.")
        
        # Optional: Bestätigung an Lehrkraft senden
        send_teacher_confirmation(booking_data, teacher_email)
        
        return True
        
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")
        return False

def send_teacher_confirmation(booking_data, teacher_email):
    """Sendet eine Bestätigung an die Lehrkraft"""
    
    if not SMTP_USER or not SMTP_PASS or SMTP_HOST == 'smtp.example.com':
        return  # SMTP nicht konfiguriert
    
    try:
        students_list = "\n".join([
            f"  - {s['name']} (Klasse {s['klasse']})" 
            for s in booking_data['students']
        ])
        
        subject = f"Buchungsbestätigung SportOase - {booking_data['date']}"
        body = f"""
Ihre Buchung wurde erfolgreich registriert:

Datum: {booking_data['date']} ({booking_data['weekday']})
Stunde: {booking_data['period']}. Stunde
Angebot: {booking_data['offer_label']}

Angemeldete Schüler:
{students_list}

Vielen Dank für Ihre Buchung!

---
Diese E-Mail wurde automatisch vom SportOase-Buchungssystem generiert.
"""
        
        msg = MIMEMultipart()
        msg['From'] = SMTP_FROM
        msg['To'] = teacher_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"Bestätigungs-E-Mail an {teacher_email} gesendet.")
        
    except Exception as e:
        print(f"Fehler beim Versand der Bestätigung: {e}")
