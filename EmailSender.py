import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
            msg.attach(MIMEText(message, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send the message
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            server.quit()

            # Return confirmation message
            return f"Email sent successfully to {recipient_email}."
        except Exception as e:
            # Return error message in case of failure
            return f"Failed to send email to {recipient_email}. Error: {str(e)}"
