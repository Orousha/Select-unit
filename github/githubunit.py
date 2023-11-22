import sqlite3
# # ---------------CREATE stusents TABLE----------
# cnt = sqlite3.connect("students.db")
# sql = '''CREATE TABLE students(
#     id INTEGER PRIMARY KEY,
#     user VARCHAR(30) NOT NULL,
#     pass VARCHAR(20) NOT NULL,
#     dars text 
#     )'''

# cnt.execute(sql)
# -------------------------------------

# ------------CREATE UNITS TABLE---------
cnt = sqlite3.connect("students.db")

# sql = '''CREATE TABLE units(
#     id INTEGER PRIMARY KEY,
#     unitname VARCHAR(30) NOT NULL,
#     vahed INTEGER NOT NULL
#     )'''

# cnt.execute(sql)
# print("done!")

sql = '''INSERT INTO units(unitname,vahed)
    VALUES("Datastructure",3)'''
cnt.execute(sql)
cnt.commit()
print("data inserted.")
# # ---------------------------------------
