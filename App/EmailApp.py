import streamlit as st
import pandas as pd
from EmailChunker import EmailChunker
from EmailSender import EmailSender
from crm_database import CRMDatabase
import Client

def run_email_app(app_type):
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    path = '/home/anisse9/vpn/'
    email_sender = EmailSender(sender_email, sender_password)
    bdd = CRMDatabase()

    if app_type == "Group send":
        run_group_send(email_sender, path, bdd)
    elif app_type == "Single send":
        run_single_send(email_sender, bdd)
    elif app_type == "Manage Client":
        run_manage_client(bdd)
    elif app_type == "Manage Template":
        run_manage_template(bdd)

# page group send 
def run_group_send(email_sender, path, bdd):
    st.write("### Group send")
    tab1, tab2 = st.tabs(["From excel file", "From database"])
    with tab1:
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

            df_to_all = pd.DataFrame(bdd.get_all_template_one_to_all(),columns=["template_name","template_content","type_template"])
            options = df_to_all['template_name'].to_list()
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

    with tab2: # From database
        st.write("### From database ")
        serie_email_file = pd.DataFrame(bdd.get_all_clients(), columns=["id_client","email","user_name","password","recovery_token"])
        chunker = EmailChunker(chunk_size=298)
        chunked_email_array = chunker.chunk_emails(serie_email_file["email"])  # split the email addresses into chunks
        moy_email = len(chunked_email_array[0])  # calculate the average number of emails per chunk
        nbr_groupe = len(chunked_email_array)  # calculate the number of chunks
        st.write(f" ### There are {nbr_groupe} groups of {moy_email} emails, for a total of {nbr_groupe * moy_email} emails")
        st.write(f"### The estimated duration of sending emails is: {nbr_groupe / 24} days") 
        if st.button("show email list "):
            st.write(serie_email_file)
        #TO modifier 
        
        
        



        st.write('####  0) select tempalte ') 
        df_to_all = pd.DataFrame(bdd.get_all_template_one_to_all(),columns=["template_name","template_content","type_template"])
        options = df_to_all['template_name'].to_list()
        selected_option = st.selectbox('Choose an option:', options)
        html_content = df_to_all[df_to_all["template_name"]==selected_option]["template_content"]
        indexe = html_content.index.to_list()[0]
        if selected_option :
            st.markdown(html_content[indexe], unsafe_allow_html=True) 
            
            

        if st.button("Send test email"):
            for list_email in chunked_email_array[:2]:
                for i, email in enumerate(list_email):          
                        email_sender.send_email( email, "testh_helmi_html", html_string)
                st.write("envoyé")
        else:
            pass

        st.write('####  1) envoyé a tout le monde')
        st.write('####  2) envoyer au restes contact pas encore envoyé')

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
    tab1, tab2, tab3 = st.tabs(["Manage clients","Client data", "Add clients from excel to the BDD"])
    with tab1:
        st.write("### Create Client")
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
    
    with tab2: # Client data
        st.write("Client data ")
        # Search client 
        st.write("### Search client")
        with st.expander("Search client"):
            with st.form("Search Form"):
                search_input = st.text_input("Enter the username or email to search")
                search_button = st.form_submit_button("Search")
                
            if search_button:
                if search_input != "":
                    st.write("Data from :", search_input)

            if st.button("tous les client"):
                st.write(pd.DataFrame(bdd.get_all_clients(), columns=["id_client",
                                                                        "email",
                                                                        "user_name",
                                                                        "password",
                                                                        "recovery_token"]
                                                                        )) 
        
    with tab3:
        st.write("insert code for insert client from file")
        #exracte data from file
        file = st.file_uploader("Excel file")  
             
        if file is not None: 
            file_extracted = pd.read_excel(file)
            st.write(file_extracted.columns[0])
            try :

                if  file_extracted.columns[0] == "email":
                    st.write("fichicher avec seulement les emails ")
                elif  file_extracted.columns[1] == "username":
                    st.write("crée un client et l'intégrer dans la base de donné")             
                
            except IndexError:
                st.write("autres fichiers")           
            
        #client = Client(email, username, password, recovery_token=None)

    
            
def run_manage_template(bdd) :
    
    # Utilisation dans Streamlit
    

    tab1, tab2 = st.tabs(["Add tempalte html ","Manage template"])

    with tab1 :
        file_upload = st.file_uploader("Sélectionnez le fichier HTML", type=["html"])   
        if file_upload is not None:
            template_name = st.text_input("Nom du template")
            type_template = st.selectbox("Type de template", ['one-to-all', 'one-to-one'])
            if st.button("Insérer dans la base de données"):                       
                bdd.create_template(template_name, file_upload.getvalue().decode('utf-8'), type_template)
                bdd.close()
                st.success("Le template a été inséré dans la base de données avec succès.")

    with tab2 :
        st.write("### Manage tempalte")
        if st.button("show tempalte"):  
            df_template = pd.DataFrame(bdd.get_all_template(), columns=["id_template", "name_template","type_template"])      
            st.write(df_template)
        if st.button("delate template "):
            with st.expander("Delete template"):
                with st.form("delete template"):
                    id_template = st.number_input("Enter id_template")                    
                    delete_button = st.form_submit_button("delete")
                    
            if delete_button:
                bdd.delete_template(int(id_template))
                bdd.close()
                st.success("Username deleated :", df_template["id_template"]==id_template)



    # add a single template
    # add a multiple template
    # liste a template  


    
    
