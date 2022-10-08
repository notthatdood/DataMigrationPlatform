#!/usr/bin/python 
#code from: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
import mariadb 

conn = mariadb.connect(
    user="admin",
    password="password",
    host="localhost",
    port=3306,
    database="test-db")
cur = conn.cursor() 

#retrieving information 
some_name = "Maria" 
#Create a table
#try: 
cur.execute("CREATE OR REPLACE TABLE employees (id int auto_increment,first_name varchar(255) not null,last_name varchar(255) not null, primary key(id));")
#except mariadb.Error as e: 
    #print(f"Error: {e}")


#insert information 
try: 
    cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria","DB")) 
except mariadb.Error as e: 
    print(f"Error: {e}")

#query information
try: 
    cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,)) 
except mariadb.Error as e: 
    print(f"Error: {e}")
for first_name, last_name in cur: 
    print(f"First name: {first_name}, Last name: {last_name}")
    

conn.commit() 
print(f"Last Inserted ID: {cur.lastrowid}")
    
conn.close()