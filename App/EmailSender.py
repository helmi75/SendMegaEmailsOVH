import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime



class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_email, subject, message):
        try:
            # OVH SMTP server settings
            smtp_server = 'ssl0.ovh.net'
            smtp_port = 587

            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach HTML message
            msg.attach(MIMEText(message, 'html'))       

            # Connect to SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send the message
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            server.quit()

            # Return confirmation message
            return True
        except Exception as e:
            # Return error message in case of failure
            return e
        
    def get_mail(self):
        try:
            # Connexion au serveur IMAP d'OVH
            imap_server = 'ssl0.ovh.net'
            imap_port = 993

            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(self.sender_email, self.sender_password)

            # Sélection de la boîte aux lettres
            mail.select('INBOX')

            # Recherche de tous les e-mails
            status, email_ids = mail.search(None, 'ALL')

            if status == 'OK':
                email_ids = email_ids[0].split()
                all_emails = []

                for email_id in email_ids:
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        raw_email = email_data[0][1]
                        msg = email.message_from_bytes(raw_email)

                        # Extraire les informations de l'e-mail (sujet, expéditeur, etc.)
                        subject, encoding = decode_header(msg['Subject'])[0]
                        #subject = subject.decode(encoding or 'utf-8')
                        from_name, from_email = email.utils.parseaddr(msg['From'])

                        # Récupérer la date de réception de l'e-mail avec gestion des erreurs
                        date_received = None
                        if 'Date' in msg:
                            try:
                                date_received = email.utils.parsedate_to_datetime(msg['Date'])
                            except Exception as date_error:
                                print(f"Erreur lors de la récupération de la date de réception : {str(date_error)}")

                        # Récupérer le contenu de l'e-mail
                        email_content = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    email_content = part.get_payload(decode=True).decode()
                        else:
                            email_content = msg.get_payload(decode=True).decode()

                        # Ajouter l'e-mail à la liste
                        all_emails.append({
                            'from_name': from_name,
                            'from_email': from_email,
                            'subject': subject,
                            'date_received': date_received,
                            'content': email_content
                        })

                return all_emails

            mail.logout()

        except Exception as e:
            return str(e)

