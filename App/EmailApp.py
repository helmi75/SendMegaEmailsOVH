import pandas as pd
import streamlit as st
from pandas import Series
from EmailChunker import EmailChunker
from EmailSender import EmailSender


def main():
    # User interface with Streamlit
    st.title("Sending emails with OVH")
    st.sidebar("salut")
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
    path='/home/anisse9/vpn/'
    options = ['King_VPN_template2.html','King_VPN_template1.html']
    selected_option = st.selectbox('Choose an option:', options)
    with open(path+selected_option, "r") as f:
        html_string = f.read()
    st.markdown(html_string, unsafe_allow_html=True)

    if st.button("Send test email"):
        for list_email in chunked_email_array[:2]:
            for i, email in enumerate(list_email):          
                    email_sender.send_email( email, "testh_helmi_html", html_string)
            st.write("envoyé")


if __name__ == "__main__":
    main()