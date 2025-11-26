import os
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM,
                    ADMIN_EMAIL)

# =====================================================================
#  SMTP SENDEN (SSL, Port 465)
# =====================================================================


def send_email_smtp(to_email, subject, body_html, body_text=None):
    logger = logging.getLogger(__name__)

    logger.info(f"Versuche E-Mail zu senden an: {to_email}")
    logger.info(f"SMTP_USER gesetzt: {bool(SMTP_USER)}")
    logger.info(f"SMTP_PASS gesetzt: {bool(SMTP_PASS)}")

    try:
        if not SMTP_USER or not SMTP_PASS:
            print("[EMAIL] WARNUNG: SMTP ist nicht korrekt konfiguriert.")
            return False

        # SSL-Verbindung (Port 465) - besser für gehostete Umgebungen
        print(f"[EMAIL] Verbinde mit {SMTP_HOST}:465 (SSL)...")
        server = smtplib.SMTP_SSL(SMTP_HOST, 465, timeout=30)
        server.login(SMTP_USER, SMTP_PASS)

        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject

        if body_text:
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

        msg.attach(MIMEText(body_html, "html", "utf-8"))

        server.send_message(msg)
        server.quit()

        print(f"[EMAIL] Erfolgreich gesendet an {to_email}")
        return True

    except Exception as e:
        print(f"[EMAIL] FEHLER beim E-Mail-Versand an {to_email}: {e}")
        return False


# =====================================================================
#  BUCHUNGSMELDUNG (ADMIN)
# =====================================================================


def create_booking_notification_email(data):
    teacher = data.get("teacher_name", "Unbekannt")
    teacher_class = data.get("teacher_class", "")
    date = data.get("date", "")
    weekday = data.get("weekday", "")
    period = data.get("period", "")
    offer = data.get("offer_label", "")
    offer_type = data.get("offer_type", "")

    students_json = data.get("students_json", "[]")
    students = json.loads(students_json) if isinstance(students_json,
                                                       str) else students_json
    count = len(students)

    students_html = "<br>".join(
        [f"• {s['name']} (Klasse {s['klasse']})"
         for s in students]) if students else "Keine Schüler"
    students_list = ", ".join(
        [f"{s['name']} ({s['klasse']})"
         for s in students]) if students else "Keine Schüler"

    subject = f"📅 SportOase Buchung: {offer} am {date}"

    html = f"""
    <html><body>
        <h2 style="background:#3b82f6;color:white;padding:10px;border-radius:8px;">
            Neue Buchung – SportOase
        </h2>
        <p><b>Lehrkraft:</b> {teacher} {f"({teacher_class})" if teacher_class else ""}</p>
        <p><b>Datum:</b> {date} ({weekday})</p>
        <p><b>Stunde:</b> {period}. Stunde</p>
        <p><b>Angebot:</b> {offer} – <span style="color:#3b82f6">{offer_type.upper()}</span></p>
        <h3>Schüler ({count}):</h3>
        <p>{students_html}</p>
    </body></html>
    """

    text = f"""
Neue Buchung – SportOase

Lehrkraft: {teacher}
Datum: {date} ({weekday})
Stunde: {period}. Stunde
Angebot: {offer} ({offer_type})

Schüler ({count}):
{students_list}
    """

    return subject, html, text


def send_booking_notification(data):
    subject, html, text = create_booking_notification_email(data)
    return send_email_smtp(ADMIN_EMAIL, subject, html, text)


# =====================================================================
#  BENUTZER-BESTÄTIGUNG
# =====================================================================


def create_user_confirmation_email(data):
    teacher = data.get("teacher_name", "Unbekannt")
    teacher_class = data.get("teacher_class", "")
    date = data.get("date", "")
    weekday = data.get("weekday", "")
    period = data.get("period", "")
    offer = data.get("offer_label", "")
    offer_type = data.get("offer_type", "")

    students_json = data.get("students_json", "[]")
    students = json.loads(students_json) if isinstance(students_json,
                                                       str) else students_json
    count = len(students)

    students_html = "<br>".join(
        [f"• {s['name']} (Klasse {s['klasse']})"
         for s in students]) if students else "Keine Schüler"

    subject = f"Buchungsbestätigung: {offer} am {date}"

    html = f"""
    <html><body>
        <h2 style="background:#C2185B;color:white;padding:10px;border-radius:8px;">
            Buchungsbestätigung – SportOase
        </h2>
        <p><b>Ihre Buchung wurde erfolgreich gespeichert!</b></p>
        <p><b>Datum:</b> {date} ({weekday})</p>
        <p><b>Stunde:</b> {period}. Stunde</p>
        <p><b>Angebot:</b> {offer} – {offer_type.upper()}</p>
        <h3>Schüler ({count}):</h3>
        <p>{students_html}</p>
    </body></html>
    """

    text = f"""
Buchungsbestätigung – SportOase

Ihre Buchung wurde erfolgreich gespeichert!

Datum: {date} ({weekday})
Stunde: {period}. Stunde
Angebot: {offer} ({offer_type})

Schüler ({count}):
{", ".join([f"{s['name']} ({s['klasse']})" for s in students])}
    """

    return subject, html, text


def send_user_booking_confirmation(email, data):
    subject, html, text = create_user_confirmation_email(data)
    return send_email_smtp(email, subject, html, text)
