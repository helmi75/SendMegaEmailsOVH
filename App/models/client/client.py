import sqlite3
from .crm_database import CRMDatabase



class CreateClient(CRMDatabase):

    def create_client(self, email, user_name=None, password=None, recovery_token=None, group_name=None):
        self.cursor.execute("INSERT INTO client (email, user_name, password, recovery_token, group_name) VALUES (?, ?, ?, ?, ?)",
                            (email, user_name, password, recovery_token, group_name))
        self.conn.commit()

    def delete_client(self, id_client):
        self.cursor.execute("DELETE FROM client WHERE id_client = ?", (id_client,))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM client")
        return self.cursor.fetchall()
    
    
    
    def get_id_client(self, email):
        self.cursor.execute("SELECT id_client FROM client WHERE email = ?", (email,)) 
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
