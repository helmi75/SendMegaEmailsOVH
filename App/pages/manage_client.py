import streamlit as st
import pandas as pd 

# Page Manage Client
def run_manage_client(client):
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
                client.create_client(email, user_name, password, recovery_token)
                st.write("Username created:", user_name)

        # deleate client 
        st.write("### Delete client")
        with st.expander("Delete client"):
            with st.form("Delete Form"):
                delete_input_id = st.text_input("Enter id client")         
                delete_button = st.form_submit_button("Delete")    
        if delete_button:
            if delete_input_id != "":
                client.delete_client(int(delete_input_id) )
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
                st.write(pd.DataFrame(client.get_all_clients(), columns=["id_client",
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
            
        if st.button("Insert a new client"):
           
           for i, email in enumerate(file_extracted["email"]):
                client.create_client(email, user_name, password, recovery_token=None)
                st.write(f"{i} email: {email} ")

if __name__ == "__main__":
    run_manage_client("Manage Client")