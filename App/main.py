import streamlit as st
from EmailSender import EmailSender
from models.client.client import  CreateClient
from models.client.message import CreateMessage 
from models.client.template import  CreateTemplate
from pages.group_send import run_group_send
from pages.single_send import run_single_send
from pages.manage_client import run_manage_client
from pages.manage_template import run_manage_template



def run_email_app(app_type):
    sender_email = "contact@kingvpn.fr"
    sender_password = "Bizerte7000"
    path = '/home/anisse9/vpn/'
    email_sender = EmailSender(sender_email, sender_password)
    #bdd = CRMDatabase()

    message = CreateMessage() 
    client = CreateClient() 
    template = CreateTemplate()

    if app_type == "Group send":
        run_group_send(email_sender, client, template)
    elif app_type == "Single send":
        run_single_send(email_sender, template)
    elif app_type == "Manage Client":
        run_manage_client( client)
    elif app_type == "Manage Template":
        run_manage_template( template)



def main():
    st.title("Sending emails with OVH") 
    add_selectbox = st.sidebar.selectbox(
        "Choose your goal",
        ("Group send", "Single send", "Manage Client","Manage Template")
    )

    if add_selectbox == "Group send":
        run_email_app("Group send")
    elif add_selectbox == "Single send":
        run_email_app("Single send")
    elif add_selectbox == "Manage Client":
        run_email_app("Manage Client")
    elif add_selectbox == "Manage Template":
        run_email_app("Manage Template")

if __name__ == "__main__":
    main()
