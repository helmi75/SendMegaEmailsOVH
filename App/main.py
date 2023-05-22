import streamlit as st
from EmailApp import run_email_app


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
