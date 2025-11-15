import os
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
from datetime import datetime

def get_gmail_access_token():
    """Holt das Access Token von der Replit Gmail Integration"""
    try:
        hostname = os.environ.get('REPLIT_CONNECTORS_HOSTNAME')
        x_replit_token = None
        
        if os.environ.get('REPL_IDENTITY'):
            x_replit_token = 'repl ' + os.environ['REPL_IDENTITY']
        elif os.environ.get('WEB_REPL_RENEWAL'):
            x_replit_token = 'depl ' + os.environ['WEB_REPL_RENEWAL']
        
        if not x_replit_token or not hostname:
            print("Gmail Integration nicht verfügbar - verwende Fallback SMTP")
            return None
        
        import requests
        response = requests.get(
            f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=google-mail',
            headers={
                'Accept': 'application/json',
                'X_REPLIT_TOKEN': x_replit_token
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('items') and len(data['items']) > 0:
                connection = data['items'][0]
                access_token = connection.get('settings', {}).get('access_token') or \
                             connection.get('settings', {}).get('oauth', {}).get('credentials', {}).get('access_token')
                return access_token
        
        return None
    except Exception as e:
        print(f"Fehler beim Abrufen des Gmail Access Tokens: {e}")
        return None

def send_gmail_notification(to_email, subject, body_html, body_text=None):
    """Sendet eine Email-Benachrichtigung über Gmail API"""
    try:
        access_token = get_gmail_access_token()
        
        if not access_token:
            print("WARNUNG: Kein Gmail Access Token verfügbar - Email wird nicht gesendet")
            print("Stellen Sie sicher, dass die Gmail-Integration eingerichtet ist")
            return False
        
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials(token=access_token)
        
        service = build('gmail', 'v1', credentials=creds)
        
        message = MIMEMultipart('alternative')
        message['To'] = to_email
        message['From'] = 'me'
        message['Subject'] = subject
        
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            message.attach(part1)
        
        part2 = MIMEText(body_html, 'html')
        message.attach(part2)
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"Email erfolgreich gesendet an {to_email}: {send_message['id']}")
        return True
        
    except Exception as e:
        print(f"Fehler beim Senden der Gmail-Nachricht: {e}")
        return False

def create_booking_notification_email(booking_data):
    """Erstellt eine formatierte Email-Benachrichtigung für eine neue Buchung"""
    teacher_name = booking_data.get('teacher_name', 'Unbekannt')
    teacher_class = booking_data.get('teacher_class', '')
    date = booking_data.get('date', '')
    period = booking_data.get('period', '')
    offer_label = booking_data.get('offer_label', '')
    offer_type = booking_data.get('offer_type', '')
    
    students = []
    try:
        students_json = booking_data.get('students_json', '[]')
        students = json.loads(students_json) if isinstance(students_json, str) else students_json
    except:
        students = []
    
    students_count = len(students)
    
    if students:
        students_names = ', '.join([f"{s['name']} ({s['klasse']})" for s in students])
    else:
        students_names = 'Keine Schüler angegeben'
    
    subject = f"📅 Neue Buchung: {offer_label} am {date}"
    
    body_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%); 
                       color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .header h2 {{ margin: 0; }}
            .content {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
            .info-row {{ margin: 10px 0; padding: 10px; background: white; border-radius: 4px; }}
            .label {{ font-weight: bold; color: #38bdf8; }}
            .students-list {{ margin-top: 10px; padding-left: 20px; }}
            .footer {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; 
                      text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🏫 SportOase - Neue Buchung</h2>
            </div>
            <div class="content">
                <div class="info-row">
                    <span class="label">👤 Lehrkraft:</span> {teacher_name}
                    {f' ({teacher_class})' if teacher_class else ''}
                </div>
                <div class="info-row">
                    <span class="label">📅 Datum:</span> {date}
                </div>
                <div class="info-row">
                    <span class="label">🕐 Stunde:</span> Stunde {period}
                </div>
                <div class="info-row">
                    <span class="label">📋 Angebot:</span> {offer_label}
                    <span style="background: {'#4ade80' if offer_type == 'fest' else '#60a5fa'}; 
                                 color: white; padding: 2px 8px; border-radius: 12px; 
                                 font-size: 11px; margin-left: 8px;">
                        {offer_type.upper()}
                    </span>
                </div>
                <div class="info-row">
                    <span class="label">👥 Anzahl Schüler:</span> {students_count}
                    <div class="students-list">
                        {students_names}
                    </div>
                </div>
            </div>
            <div class="footer">
                <p>Diese Nachricht wurde automatisch vom SportOase Buchungssystem generiert.</p>
                <p>Zeit: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    body_text = f"""
SportOase - Neue Buchung

Lehrkraft: {teacher_name} {f'({teacher_class})' if teacher_class else ''}
Datum: {date}
Stunde: Stunde {period}
Angebot: {offer_label} ({offer_type.upper()})
Anzahl Schüler: {students_count}
Schüler: {students_names}

Zeit: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}
    """
    
    return subject, body_html, body_text

def send_booking_notification(booking_data, admin_email):
    """Sendet eine Buchungsbenachrichtigung an den Admin"""
    try:
        subject, body_html, body_text = create_booking_notification_email(booking_data)
        return send_gmail_notification(admin_email, subject, body_html, body_text)
    except Exception as e:
        print(f"Fehler beim Senden der Buchungsbenachrichtigung: {e}")
        return False
