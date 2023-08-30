import sqlite3
from .crm_database import CRMDatabase



class CreateTemplate(CRMDatabase):
    
    def create_template(self, template_name, template_content, type_template):
        self.cursor.execute("INSERT INTO template (template_name, template_content, type_template) VALUES (?, ?, ?)",
                            (template_name, template_content, type_template))
        self.conn.commit()

    def delete_template(self, id_template):
        self.cursor.execute("DELETE FROM template WHERE id_template =  VALUES (?)", (id_template))
        self.conn.commit()

    def get_all_template_one_to_one(self):
        self.cursor.execute("SELECT template_name, template_content, type_template FROM template where type_template='one-to-one'")
        return self.cursor.fetchall()
    
    def get_all_template_one_to_all(self):
        self.cursor.execute("SELECT template_name, template_content, type_template FROM template where type_template='one-to-all'")
        return self.cursor.fetchall()
    
    def get_all_template(self):
        self.cursor.execute("SELECT id_template,template_name,type_template  FROM template")
        return self.cursor.fetchall()