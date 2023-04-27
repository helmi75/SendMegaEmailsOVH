import pandas as pd 
import streamlit as st
from pandas import Series
import numpy as np


def chunk_fonction(emails: Series) -> np.ndarray:
    """
    Cette fonction divise une pandas.Series en un numpy.ndarray contenant des chunks de même taille.
    """
    chunk_size = 298
    num_chunks = int(np.ceil(len(emails) / chunk_size)) # arrondir à l'entier supérieur
    chunks = np.array_split(emails, num_chunks)
    return chunks



# Interface utilisateur avec Streamlit
st.title("Envoi d'e-mails avec OVH")

# Entrées de l'utilisateur
sender_email = st.text_input("Adresse e-mail de l'expéditeur")
sender_password = st.text_input("Mot de passe de l'expéditeur", type='password')
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
       #recipient_emails = st.text_input("Adresses e-mail des destinataires (séparées par des virgules)")
       subject = f"Sujet de l'e-mail num {i}"
       with open('mail.html', 'r') as f:
           message = f.read()
       st.write(f' email envoyer à {email}') 
       st.write(f'sujet {subject}') 
       st.markdown(message.format(mail= email), unsafe_allow_html=True)
# Bouton pour envoyer les e-mails
if st.button("Envoyer"):
    # Séparation des adresses e-mail en une liste
    recipient_emails_list = recipient_emails.split(",")
    
    # Envoi des e-mails à chaque destinataire
    for recipient_email in recipient_emails_list:
        st.write(send_email(sender_email, sender_password, recipient_email.strip(), subject, message))

