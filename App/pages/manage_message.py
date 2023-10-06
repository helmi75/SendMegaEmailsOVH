import streamlit as st
import htmlmin
from datetime import datetime


def run_manage_message(messagess):


    st.title("Simple chat")
    user = st.selectbox("selectionner un email ", 
                        ["helmichiha@gmail.com","contact@kingvpn.fr"])
   
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for messaga in messagess.get_test_message(user):        
        with st.chat_message("user"):
            active_user = messaga[0]
            active_content = htmlmin.minify(messaga[1])
            active_date = messaga[2]
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
            st.write(f'{active_content}',unsafe_allow_html=True)

    

    

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message(name="human", avatar="🧑‍💻"):
            st.markdown(f'users :  helmi ')          
            st.markdown(f'{datetime.now()}')
            
        
        st.session_state.messages.append({"role": "", "content": prompt}) 