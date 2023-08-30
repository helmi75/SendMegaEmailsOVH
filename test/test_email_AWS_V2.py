import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Paramètres SMTP d'Amazon SES
smtp_server = 'email-smtp.us-east-1.amazonaws.com'
smtp_port = 587
smtp_username = 'AKIAYQFIMXQIAGORJ7GO'
smtp_password = 'BP41rOuaKAJg0x0vmHAZpeiOu/2fidB1NH3hw+lCoeOW'

# Créer un objet MIMEMultipart pour l'e-mail
message = MIMEMultipart()
message['From'] = 'contact@kingvpn.fr'
message['To'] = 'contact@helmane.fr'
message['Subject'] = 'Sujet de l\'e-mail'

# Corps de l'e-mail (HTML)
body = """
<html>
<head></head>
<body>
  <h1>Amazon SES Test</h1>
  <p>Ceci est un e-mail de test envoyé via Amazon SES en utilisant SMTP.</p>
</body>
</html>
"""
message.attach(MIMEText(body, 'html'))

# Établir une connexion SMTP et envoyer l'e-mail
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Démarrer une connexion TLS
    server.login(smtp_username, smtp_password)
    server.sendmail(message['From'], message['To'], message.as_string())

print("E-mail envoyé avec succès")
