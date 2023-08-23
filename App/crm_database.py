import sqlite3

class CRMDatabase:
    def __init__(self, db_name='/home/anisse9/vpn/App/crm.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_client(self, email, user_name, password, recovery_token):
        self.cursor.execute("INSERT INTO client (email, user_name, password, recovery_token) VALUES (?, ?, ?, ?)",
                            (email, user_name, password, recovery_token))
        self.conn.commit()

    def delete_client(self, id_client):
        self.cursor.execute("DELETE FROM client WHERE id_client = ?", (id_client,))
        self.conn.commit()

    def create_message(self, id_client, message_sended, date):
        self.cursor.execute("INSERT INTO message (id_client, message_sended, date) VALUES (?, ?, ?)",
                            (id_client, message_sended, date))
        self.conn.commit()

    def delete_message(self, id_message):
        self.cursor.execute("DELETE FROM message WHERE id_message = ?", (id_message,))
        self.conn.commit()

    def insert_message(self, id_client, message_sended, date):
        self.cursor.execute("INSERT INTO message (id_client, message_sended, date)VALUES (?, ?, ?)",
                             (id_client, message_sended, date))
        self.conn.commit()

    def get_all_messages(self):
        self.cursor.execute("SELECT * FROM message")
        return self.cursor.fetchall()


    def create_template(self, template_name, template_content, type_template):
        self.cursor.execute("INSERT INTO template (template_name, template_content, type_template) VALUES (?, ?, ?)",
                            (template_name, template_content, type_template))
        self.conn.commit()

    def delete_template(self, id_template):
        self.cursor.execute("DELETE FROM template WHERE id_template =  VALUES (?)", (id_template))
        self.conn.commit()
    
    

    def close(self):
        self.conn.close()
        
    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM client")
        return self.cursor.fetchall()
    
    def get_all_template_one_to_one(self):
        self.cursor.execute("SELECT template_name, template_content, type_template FROM template where type_template='one-to-one'")
        return self.cursor.fetchall()
    
    def get_all_template_one_to_all(self):
        self.cursor.execute("SELECT template_name, template_content, type_template FROM template where type_template='one-to-all'")
        return self.cursor.fetchall()
    
    def get_all_template(self):
        self.cursor.execute("SELECT id_template,template_name,type_template  FROM template")
        return self.cursor.fetchall()