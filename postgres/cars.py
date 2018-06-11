import psycopg2
import sys

con = None

try:
    con = psycopg2.connect(database='pos')
    cur = con.cursor()
    
    cur.execute('''
        CREATE TABLE cars (id INT PRIMARY KEY, name VARCHAR(20), price INT)
    ''')
    cur.execute('''
        INSERT INTO cars VALUES (1,'Audi',24000)
    ''')
    cur.execute('''
        INSERT INTO cars VALUES (2,'Skoda',9000)
    ''')
    cur.execute('''
        INSERT INTO cars VALUES (3,'Dacia',7000)
    ''')

    cur.execute('''
        INSERT INTO cars VALUES (4,'Lada',7000)
    ''')
    con.commit()
    print('Three cars inserted')

    cars = (
        (5,'Fiat',9340),        
        (6,'Volvo',9340),        
        (7,'Citroen',9340),        
    )
    query = 'INSERT INTO cars (id,name,price) VALUES(%s,%s,%s)'
    cur.executemany(query,cars)
    con.commit()
    print('Another three cars inserted')
except psycopg2.DatabaseError:
    if con:
        con.rollback()

finally:
    if con:
        con.close()
