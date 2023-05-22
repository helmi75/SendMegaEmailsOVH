import pandas as pd
import streamlit as st
from pandas import Series
from EmailChunker import EmailChunker
from EmailSender import EmailSender
from crm_database import CRMDatabase


def main():
    # User interface with Streamlit
    
    st.title("Sending emails with OVH") 
    add_selectbox = st.sidebar.selectbox(
    "choise your gols",
    ("Group send", "Single send",'Client BDD')) 

    # User inputs
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    path='/home/anisse9/vpn/'
    email_sender = EmailSender(sender_email, sender_password)
    bdd = CRMDatabase()
    
    if add_selectbox == "Group send":   
        file = st.file_uploader("Excel file")  # upload an excel file containing email addresses
        if file is not None:
            serie_email_file = pd.read_excel(file)  # read the excel file with pandas
            chunker = EmailChunker(chunk_size=298)
            chunked_email_array = chunker.chunk_emails(serie_email_file["email"])  # split the email addresses into chunks
            moy_email = len(chunked_email_array[0])  # calculate the average number of emails per chunk
            nbr_groupe = len(chunked_email_array)  # calculate the number of chunks
            st.write(f" ### There are {nbr_groupe} groups of {moy_email} emails, for a total of {nbr_groupe * moy_email} emails")
            st.write(f"### The estimated duration of sending emails is: {nbr_groupe / 24} days")

            
            
            options = ['King_VPN_template1.html']
            selected_option = st.selectbox('Choose an option:', options)
            if selected_option == 'King_VPN_template1.html':
                with open(path+selected_option, "r") as f:
                    html_string = f.read()
                st.markdown(html_string, unsafe_allow_html=True)

            if st.button("Send test email"):
                for list_email in chunked_email_array[:2]:
                    for i, email in enumerate(list_email):          
                            email_sender.send_email( email, "testh_helmi_html", html_string)
                    st.write("envoyé")
            else:
                pass
    elif add_selectbox == "Single send" :
        options = ['King_VPN_template2.html']
        selected_option = st.selectbox('Choose an option:', options)
        if selected_option == 'King_VPN_template2.html':
            email = st.text_input("email")
            user_name = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe")  
            recovery_token =   st.text_input("Token de récupération ") 
            with open(path+selected_option, "r") as f:
                html_string = f.read()
            html_string = html_string.format(user_name=user_name, password=password, recovery_token=recovery_token)
            st.markdown(html_string, unsafe_allow_html=True)

        if st.button("Send test email"):
            email_sender.send_email(email, "testh_helmi_html", html_string)
            st.write("envoyé")

    elif add_selectbox == "Client BDD" :

        # create client 
        st.write("### Create client")
        with st.expander("Create client"):
            with st.form("create Form"):
                email = st.text_input("Enter email")
                user_name = st.text_input("Username")
                password = st.text_input("password")
                recovery_token = st.text_input("recovery_token")
                create_button = st.form_submit_button("Create")
            
                
        if create_button:
            # !! ajouter un test de d'insertion
                bdd.create_client(email, user_name, password, recovery_token)
                st.write("Username created:", user_name)


        # deleate client 
        st.write("### Delete client")
        with st.expander("Delete client"):
            with st.form("Delete Form"):
                delete_input_id = st.text_input("Enter id client")
                

                delete_button = st.form_submit_button("Delete")
        
        if delete_button:
            if delete_input_id != "":
                bdd.delete_client(int(delete_input_id) )
                st.write("Username deleted:", delete_input_id)


       
        # Search client 
        st.write("### Search client")
        with st.expander("Search client"):
            with st.form("Search Form"):
                search_input = st.text_input("Enter the username or email to search")
                search_button = st.form_submit_button("Search")
                
            if search_button:
                if search_input != "":
                    st.write("Username deleted:", search_input)

            if st.button("tous les client"):
                st.write(pd.DataFrame(bdd.get_all_clients(), columns=["id_client",
                                                                        "email",
                                                                        "user_name",
                                                                        "password",
                                                                        "recovery_token"]
                                                                        ))       
    

if __name__ == "__main__":
    main()