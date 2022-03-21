import sqlite3

connection = sqlite3.connect('ci_archive.db')
with open('CI10X-Archive_create.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO roles (role_description) VALUES (?)", ('Student',))
cur.execute("INSERT INTO roles (role_description) VALUES (?)", ('Faculty',))

connection.commit()
connection.close()