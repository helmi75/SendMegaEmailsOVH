import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


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
