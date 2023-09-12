import sqlite3
from .crm_database import CRMDatabase



class CreateMessage(CRMDatabase):

    def create_message(self, id_client, message_sended, date, message_status):
        self.cursor.execute("INSERT INTO message (id_client, message_sended, date, message_status) VALUES (?, ?, ?, ?)",
                            (id_client, message_sended, date, message_status))
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
    