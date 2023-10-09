import streamlit as st
import htmlmin
from datetime import datetime




def run_manage_message(email_sender, messagess, client): 

    tab1, tab2 = st.tabs(["Chat","emails"])
    with tab1:
        st.title("Simple chat")
        contact_client = [elm[1]  for elm in client.get_all_clients()]

        
        user = st.selectbox("selectionner un email ", contact_client )
    
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for messaga in messagess.get_test_message(user):        
            with st.chat_message("user"):
                active_user = messaga[1]
                active_content = htmlmin.minify(messaga[7])
                active_date = messaga[8]
                status_message = messaga[9]
                max_page_width = 800
                css = f"""
                        <style>
                            body {{
                            max-width: {max_page_width}px;
                            margin: 0 auto; 
                            }}
                        </style>
                        """
    
                active_content = f'<html><body style="max-width:{max_page_width}px;">{active_content}</body></html>'
                st.markdown(active_user)
                st.markdown( active_date)
                st.markdown(status_message)
                st.write(f'{active_content}',unsafe_allow_html=True)

        
        
        

        # Accept user input
        """if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            with st.chat_message(name="human", avatar="🧑‍💻"):
                st.markdown(f'users :  helmi ')          
                st.markdown(f'{datetime.now()}')
                
            
            st.session_state.messages.append({"role": "", "content": prompt}) """

    with tab2:
        st.dataframe(email_sender.get_mail())