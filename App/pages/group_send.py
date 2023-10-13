import streamlit as st
import pandas as pd 
import numpy as np
from pandas import Series
from datetime import datetime


class EmailChunker:
    def __init__(self, chunk_size):
        self.chunk_size = chunk_size

    def chunk_emails(self, emails: Series) -> np.ndarray:
        """
        This function splits a pandas.Series into a numpy.ndarray containing chunks of the same size.
        """
        num_chunks = int(np.ceil(len(emails) / self.chunk_size))  # round up to the nearest integer
        chunks = np.array_split(emails, num_chunks)  # split the Series into chunks
        return chunks

def run_group_send(email_sender, client, template, message):
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

            df_to_all = pd.DataFrame(template.get_all_template_one_to_all(),columns=["template_name","template_content","type_template"])
            options = df_to_all['template_name'].to_list()
            selected_option = st.selectbox('Choose an option:', options, key=1)
            st.write(selected_option)
            if selected_option :
                html_string = df_to_all[df_to_all["template_name"]==selected_option]["template_content"].values[0]
                st.markdown(html_string, unsafe_allow_html=True)
            subject = st.text_input("insert subject ")
            if st.button("Send test email", key=4):
                for list_email in chunked_email_array:
                    for i, email in enumerate(list_email):                                
                            try:                                
                                client_email= client.get_id_client(email)[0][0]                           

                                content_to_send = f"<!DOCTYPE html><html><body>{html_string}</body></html>"

                                # try to send email ton client 
                                email_status = email_sender.send_email(email , subject , content_to_send)
                                print(email_status)

                                if email_status == True:
                                    message.create_message( client_email,
                                                         content_to_send, 
                                                         datetime.now(), 
                                                         f"Email sent successfully to {email}.")
                                    st.write("envoyé")
                                else :
                                    message.create_message( client_email, 
                                                       content_to_send,
                                                       datetime.now(), 
                                                       f"Failed to send email to {email}. Error: {str(email)}")
                                    st.write("pas envoyé ")
                            except Exception as e:
                                message.create_message( client_email, 
                                                       content_to_send,
                                                       datetime.now(), 
                                                       f"Failed to send email to {email}. Error: {str(e)}")
                                st.write( f"il y'a problème d'envoie error : {e}")

            else:
                pass

    with tab2: # From database
        st.write("### From database ")
        serie_email_file = pd.DataFrame(client.get_all_clients(), 
                                        columns=["id_client","email","user_name","password","recovery_token","group_name"])
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
        df_to_all = pd.DataFrame(template.get_all_template_one_to_all(),columns=["template_name","template_content","type_template"])
        st.dataframe(df_to_all)
        options = df_to_all['template_name'].to_list()
        selected_option = st.selectbox('Choose an option:', options, key=5)
        html_content = df_to_all[df_to_all["template_name"]==selected_option]["template_content"]
        indexe = html_content.index.to_list()[0]
        if selected_option :
            st.markdown(html_content[indexe], unsafe_allow_html=True) 
            
            

        if st.button("Send test email", key=6):
            for list_email in chunked_email_array[:2]:
                for i, email in enumerate(list_email):          
                        email_sender.send_email( email, "testh_helmi_html", html_string)
                st.write("envoyé")
        else:
            pass

        st.write('####  1) envoyé a tout le monde')
        st.write('####  2) envoyer au restes contact pas encore envoyé')

if __name__ == "__main__":
     run_group_send("Group send")