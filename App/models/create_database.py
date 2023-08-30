import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('crm.db')

# Création de la table "client"
conn.execute('''CREATE TABLE IF NOT EXISTS client
                 (id_client INTEGER PRIMARY KEY,
                 email TEXT UNIQUE,
                 user_name TEXT,
                 password TEXT,
                 recovery_token TEXT )''')

# Création de la table "message"
conn.execute('''CREATE TABLE IF NOT EXISTS message
                 (id_message INTEGER PRIMARY KEY,
                 id_client INTEGER,
                 message_sended TEXT,
                 date TEXT,
                 FOREIGN KEY(id_client) REFERENCES client(id_client))''')

# Création de la table "template"
conn.execute('''CREATE TABLE IF NOT EXISTS template
                 (id_template INTEGER PRIMARY KEY,
                 template_name TEXT UNIQUE,
                 template_content TEXT,
                 type_template TEXT NOT NULL CHECK(type_template IN ('one-to-all', 'one-to-one')))''')


# Fermeture de la connexion à la base de données
conn.close()
