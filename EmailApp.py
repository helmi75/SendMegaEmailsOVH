import pandas as pd
import streamlit as st
from pandas import Series
from EmailChunker import EmailChunker
from EmailSender import EmailSender


def main():
    # User interface with Streamlit
    st.title("Sending emails with OVH")

    # User inputs
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    file = st.file_uploader("Excel file")  # upload an excel file containing email addresses
    serie_email_file = pd.read_excel(file)  # read the excel file with pandas

    chunker = EmailChunker(chunk_size=298)
    chunked_email_array = chunker.chunk_emails(serie_email_file[0])  # split the email addresses into chunks

    moy_email = len(chunked_email_array[0])  # calculate the average number of emails per chunk
    nbr_groupe = len(chunked_email_array)  # calculate the number of chunks
    st.write(f" ### There are {nbr_groupe} groups of {moy_email} emails, for a total of {nbr_groupe * moy_email} emails")
    st.write(f"### The estimated duration of sending emails is: {nbr_groupe / 24} days")

    email_sender = EmailSender(sender_email, sender_password)

    if st.button("Send test email"):
        for list_email in chunked_email_array[:2]:
            for i, email in enumerate(list_email):
                recipient_emails_list = ["helmichiha@gmail.com","helmichiha@hotmail.com"]
                for recipient_email in  recipient_emails_list:
                    st.write(send_email(sender_email, sender_password, recipient_email, subject, message))
                st.write("envoyé")


if __name__ == "__main__":
    main()