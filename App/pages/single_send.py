import streamlit as st 

# Page sigle send 
def run_single_send(email_sender, template):
    st.write("### Single send")
    # Ajoutez votre code ici pour la fonctionnalité "Single send"
    results = template.get_all_template_one_to_one()    
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
    selected_option = st.selectbox('Choose an option:', options, key=3)
    if selected_option == 'King_VPN_template2':
        email = st.text_input("email")  
        user_name = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe")  
        recovery_token =   st.text_input("Token de récupération ") 
        html_string = template_dict[selected_option]["template_content"]
        html_string = html_string.format(user_name=user_name, password=password, recovery_token=recovery_token)
        st.markdown(html_string, unsafe_allow_html=True)

    if st.button("Send test email", key=2):
        email_sender.send_email(email, "testh_helmi_html", html_string)
        st.write("envoyé")