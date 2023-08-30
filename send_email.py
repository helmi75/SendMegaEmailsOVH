import pandas as pd 
import streamlit as st
from pandas import Series
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def chunk_fonction(emails: Series) -> np.ndarray:
    """
    Cette fonction divise une pandas.Series en un numpy.ndarray contenant des chunks de même taille.
    """
    chunk_size = 298
    num_chunks = int(np.ceil(len(emails) / chunk_size)) # arrondir à l'entier supérieur
    chunks = np.array_split(emails, num_chunks)
    return chunks

def send_email(sender_email, sender_password, recipient_email, subject, message):
    try:
        # Paramètres du serveur SMTP d'OVH
        smtp_server = 'ssl0.ovh.net'
        smtp_port = 587
        
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
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

def main():
    # Interface utilisateur avec Streamlit
    st.title("Envoi d'e-mails avec OVH")

    # Entrées de l'utilisateur
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    file  = st.file_uploader("ficher_excel")
    serie_email_file = pd.read_excel(file)
    chunked_email_array = chunk_fonction(serie_email_file[0])
    moy_email =len(chunked_email_array[0])
    nbr_groupe = len(chunked_email_array)
    st.write(f" ### il y a {nbr_groupe} groupe de {moy_email} emails,  ce qui fait au total  {nbr_groupe * moy_email} emails")
    st.write(f"### la duré d'envoi d email est de  : {nbr_groupe/24} jours ") 

    if st.button("test envoi"):
        for list_email in chunked_email_array[:2] :
            for i , email in enumerate(list_email):
                recipient_emails_list = ["helmichiha@gmail.com","helmichiha@hotmail.com"]
                subject = f"Sujet de l'e-mail num {i}"
                with open('mail.html', 'r') as f:
                    message = f.read()
                st.write(f' email envoyer à {email}') 
                st.write(f'sujet {subject}') 
                name="helmi"
                if not name :
                    name=" "
                st.markdown(message.format(mail=email, name=name ), unsafe_allow_html=True)
            # Bouton pour envoyer les e-mails
            #if st.button("Envoyer"):
            # Envoi des e-mails à chaque destinataire
                subject ="wewewe"
                recipient_emails_list = ["helmichiha@gmail.com","helmichiha@hotmail.com"]
                for recipient_email in  recipient_emails_list:
                    st.write(send_email(sender_email, 
                                        sender_password, 
                                        recipient_email,
                                        subject,
                                        f"""<!DOCTYPE html>
							<html>
                                                            <head>
                                                                <title> Kingvpn </title>
                                                            </head>
                                                            <body>
                                                               {message}
                                                            </body>
                                                        </html>
                                           """
                                        )
                             )
                st.write("envoyé")

if __name__ == "__main__":
    main()
