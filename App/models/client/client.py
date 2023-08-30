import sqlite3
from .crm_database import CRMDatabase



class CreateClient(CRMDatabase):

    def create_client(self, email, user_name, password, recovery_token):
        self.cursor.execute("INSERT INTO client (email, user_name, password, recovery_token) VALUES (?, ?, ?, ?)",
                            (email, user_name, password, recovery_token))
        self.conn.commit()

    def delete_client(self, id_client):
        self.cursor.execute("DELETE FROM client WHERE id_client = ?", (id_client,))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM client")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
