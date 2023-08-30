import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        # Paramètres du serveur SMTP d'OVH
        smtp_server = 'email-smtp.us-east-1.amazonaws.com'
        smtp_port = 587

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Envoi du message
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        # Retourne un message de confirmation
        return f"L'e-mail a été envoyé à {recipient_email} avec succès."
    except Exception as e:
        # Retourne un message d'erreur en cas d'échec
        return f"L'envoi de l'e-mail à {recipient_email} a échoué. Erreur : {str(e)}"
send_email("contact@kingvpn.fr", "Bizerte7000" , "helmichiha@gmail.com",
           "voila", "<H1>c est tout AWS </H1>")
print("sended")
