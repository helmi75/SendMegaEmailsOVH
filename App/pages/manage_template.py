import streamlit as st
import pandas as pd

def run_manage_template(template) :    
    # Utilisation dans Streamlit   
    tab1, tab2 = st.tabs(["Add tempalte html ","Manage template"])
    with tab1 :
        file_upload = st.file_uploader("Sélectionnez le fichier HTML", type=["html"])   
        if file_upload is not None:
            template_name = st.text_input("Nom du template")
            type_template = st.selectbox("Type de template", ['one-to-all', 'one-to-one'])
            if st.button("Insérer dans la base de données"):                       
                template.create_template(template_name, file_upload.getvalue().decode('utf-8'), type_template)
                template.close()
                st.success("Le template a été inséré dans la base de données avec succès.")

    

    with tab2:
        st.write("### Manage template")
        if st.button("Show template"):
            df_template = pd.DataFrame(template.get_all_template(), columns=["id_template", "name_template", "type_template"])
            st.write(df_template)
        
       


        with st.expander("Delete Template"):
            with st.form("Delete Template"):
                id_temp = st.text_input("Enter id_template")
                search_button = st.form_submit_button("Delete")
                
            if search_button:
                template.delete_template(id_temp)
                st.success("supimé")
                

        

        
        




    # add a single template
    # add a multiple template
    # liste a template  