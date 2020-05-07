import sqlite3

conn = sqlite3.connect('AiDdatabase.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved

# Create table - Login_DB
c.execute('''CREATE TABLE Login_DB(
            [user_id] INTEGER PRIMARY KEY NOT NULL,
            [username] TEXT NOT NULL, 
            [email] TEXT NOT NULL,
            [password_salt] TEXT NOT NULL,
            [password_hash] TEXT NOT NULL, 
            [date_register] date NOT NULL,
            [isActive] BOOL NOT NULL
            )''')

conn.commit()