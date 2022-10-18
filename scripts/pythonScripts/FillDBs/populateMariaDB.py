#!/usr/bin/python 
#code from: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
import mariadb 

conn = mariadb.connect(
    user="root",
    password="password",
    host="localhost",
    port=3306,
    database="test-db")
cur = conn.cursor() 

cur.execute("CREATE DATABASE IF NOT EXISTS car_db")
cur.execute("CREATE DATABASE IF NOT EXISTS people_db")
cur.execute("SHOW DATABASES")
databaseList = cur.fetchall()

for database in databaseList:
    print(database)
conn.commit() 
conn.close()
#retrieving information 
#Create a table
#try:

print("------------------this is in people_db------------------")
conn = mariadb.connect(
    user="root",
    password="password",
    host="localhost",
    database="people_db")
cur = conn.cursor() 
cur.execute("CREATE OR REPLACE TABLE persona (id int auto_increment, cedula int ,nombre varchar(255) not null, provincia varchar(255) not null, canton varchar(255) not null, primary key(id));")
try: 
    cur.execute("INSERT INTO persona (cedula, nombre, provincia, canton) VALUES (?, ?, ?, ?)", (206150538, "Nereo Campos", "Cartago", "Cartago")) 
    cur.execute("INSERT INTO persona (cedula, nombre, provincia, canton) VALUES (?, ?, ?, ?)", (206150539, "Nereo Campos1", "Cartago", "Cartago")) 
    cur.execute("INSERT INTO persona (cedula, nombre, provincia, canton) VALUES (?, ?, ?, ?)", (206150540, "Nereo Campos2", "Cartago", "Cartago")) 
    cur.execute("INSERT INTO persona (cedula, nombre, provincia, canton) VALUES (?, ?, ?, ?)", (206150541, "Nereo Campos3", "Cartago", "Cartago")) 
except mariadb.Error as e: 
    print(f"Error: {e}")
#query information
try: 
    cur.execute("SELECT * FROM persona") 
except mariadb.Error as e: 
    print(f"Error: {e}")
for row in cur: 
    print(row)

conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")
    
conn.close()

print("------------------this is in car_db------------------")
conn = mariadb.connect(
    user="root",
    password="password",
    host="localhost",
    database="car_db")

cur = conn.cursor() 
cur.execute("CREATE OR REPLACE TABLE car (id int auto_increment, owner varchar(255) not null, description varchar(255) not null, primary key(id));")


try: 
    cur.execute("INSERT INTO car (owner, description) VALUES (?, ?)", (1, "Toyota Corollacross BWC-166, Blanco Perlado")) 
    cur.execute("INSERT INTO car (owner, description) VALUES (?, ?)", (2, "Honda CRV HUJ-987, Dorado")) 
    cur.execute("INSERT INTO car (owner, description) VALUES (?, ?)", (3, "Toyota Corollacross LMN-567, Blanco Perlado")) 
except mariadb.Error as e: 
    print(f"Error: {e}")


try: 
    cur.execute("SELECT * FROM car") 
except mariadb.Error as e: 
    print(f"Error: {e}")
for row in cur: 
    print(row)
    

conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")
    
conn.close()