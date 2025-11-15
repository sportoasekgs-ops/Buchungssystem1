#!/usr/bin/env python3
"""Test-Skript für Gmail-Integration und Benachrichtigungen"""

import os
from notification_service import send_gmail_notification, send_booking_notification
from datetime import datetime

def test_simple_email():
    """Sendet eine einfache Test-Email"""
    print("=" * 50)
    print("TEST 1: Einfache Test-Email")
    print("=" * 50)
    
    admin_email = os.environ.get('ADMIN_EMAIL', 'sportoase.kg@gmail.com')
    subject = "✅ SportOase Gmail-Integration Test"
    
    body_html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%); 
                     color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .content { background: #f8f9fa; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🎉 Gmail-Integration erfolgreich!</h2>
            </div>
            <div class="content">
                <p>Die Gmail-Integration für das SportOase Buchungssystem wurde erfolgreich eingerichtet.</p>
                <p><strong>Testzeit:</strong> """ + datetime.now().strftime('%d.%m.%Y um %H:%M Uhr') + """</p>
                <p>E-Mail-Benachrichtigungen funktionieren jetzt einwandfrei! ✅</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    body_text = f"""
SportOase - Gmail-Integration Test

Die Gmail-Integration wurde erfolgreich eingerichtet.
Testzeit: {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')}

E-Mail-Benachrichtigungen funktionieren jetzt einwandfrei!
    """
    
    success = send_gmail_notification(admin_email, subject, body_html, body_text)
    
    if success:
        print(f"✅ Test-Email erfolgreich gesendet an {admin_email}")
    else:
        print(f"❌ Fehler beim Senden der Test-Email")
    
    return success

def test_booking_notification():
    """Testet eine Buchungsbenachrichtigung"""
    print("\n" + "=" * 50)
    print("TEST 2: Buchungsbenachrichtigung")
    print("=" * 50)
    
    admin_email = os.environ.get('ADMIN_EMAIL', 'sportoase.kg@gmail.com')
    
    # Simuliere Buchungsdaten
    booking_data = {
        'teacher_name': 'Max Mustermann',
        'teacher_class': '5a',
        'date': '2025-11-20',
        'period': 3,
        'offer_label': 'Basketball',
        'offer_type': 'fest',
        'students_json': '[{"name": "Anna Schmidt", "klasse": "5a"}, {"name": "Tom Müller", "klasse": "5b"}]'
    }
    
    success = send_booking_notification(booking_data, admin_email)
    
    if success:
        print(f"✅ Buchungsbenachrichtigung erfolgreich gesendet an {admin_email}")
    else:
        print(f"❌ Fehler beim Senden der Buchungsbenachrichtigung")
    
    return success

if __name__ == '__main__':
    print("\n🔍 Starte Gmail-Integration Tests...\n")
    
    # Test 1: Einfache Email
    test1_result = test_simple_email()
    
    # Test 2: Buchungsbenachrichtigung
    test2_result = test_booking_notification()
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("ZUSAMMENFASSUNG")
    print("=" * 50)
    print(f"Test 1 (Einfache Email): {'✅ BESTANDEN' if test1_result else '❌ FEHLGESCHLAGEN'}")
    print(f"Test 2 (Buchungsbenachrichtigung): {'✅ BESTANDEN' if test2_result else '❌ FEHLGESCHLAGEN'}")
    
    if test1_result and test2_result:
        print("\n🎉 Alle Tests erfolgreich! Gmail-Integration funktioniert perfekt.")
    else:
        print("\n⚠️ Einige Tests sind fehlgeschlagen. Bitte Logs prüfen.")
