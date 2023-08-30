import sqlite3

class CRMDatabase:

    def __init__(self, db_name='/home/anisse9/vpn/App/crm.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()      

    def close(self):
        self.conn.close()
