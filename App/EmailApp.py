import streamlit as st
import pandas as pd
from EmailChunker import EmailChunker
from EmailSender import EmailSender
from crm_database import CRMDatabase

def run_email_app(app_type):
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    path = '/home/anisse9/vpn/'
    email_sender = EmailSender(sender_email, sender_password)
    bdd = CRMDatabase()

    if app_type == "Group send":
        run_group_send(email_sender, path)
    elif app_type == "Single send":
        run_single_send(email_sender, bdd)
    elif app_type == "Manage Client":
        run_manage_client(bdd)
    elif app_type == "Manage Template":
        run_manage_template(bdd)

# page group send 
def run_group_send(email_sender, path):
    st.write("### Group send")
    # Ajoutez votre code ici pour la fonctionnalité "Group send"
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

# Page sigle send 
def run_single_send(email_sender, bdd):
    st.write("### Single send")
    # Ajoutez votre code ici pour la fonctionnalité "Single send"
    results = bdd.get_all_template_one_to_one()    
    template_dict = {}
    for row in results:
            template_name = row[0]
            template_content = row[1]
            type_template = row[2]
            template_dict[template_name] = {
                "template_content": template_content,
                "type_template": type_template
            }

    options = [row[0] for row in  results]
    selected_option = st.selectbox('Choose an option:', options)
    if selected_option == 'King_VPN_template2':
        email = st.text_input("email")  
        user_name = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe")  
        recovery_token =   st.text_input("Token de récupération ") 
        html_string = template_dict[selected_option]["template_content"]
        html_string = html_string.format(user_name=user_name, password=password, recovery_token=recovery_token)
        st.markdown(html_string, unsafe_allow_html=True)

    if st.button("Send test email"):
        email_sender.send_email(email, "testh_helmi_html", html_string)
        st.write("envoyé")

# Page Manage Client
def run_manage_client(bdd):
    st.write("### Manage Client")
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
            
def run_manage_template(bdd) :
    st.write("### Manage tempalte")
    # Utilisation dans Streamlit
    file_upload = st.file_uploader("Sélectionnez le fichier HTML", type=["html"])   
    if file_upload is not None:
        template_name = st.text_input("Nom du template")
        type_template = st.selectbox("Type de template", ['one-to-all', 'one-to-one'])
        if st.button("Insérer dans la base de données"):                       
            bdd.create_template(template_name, file_upload.getvalue().decode('utf-8'), type_template)
            bdd.close()
            st.success("Le template a été inséré dans la base de données avec succès.")


    # add a single template
    # add a multiple template
    # liste a template  


    
    
