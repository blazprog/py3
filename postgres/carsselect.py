import psycopg2
import psycopg2.extras #rabim, da lahko dobim rezultat kot dictionary

con = None

try:
    con = psycopg2.connect(database='pos', user='blaz') # ce ne napisem userja, bo to login user
    cur = con.cursor()
    print('Fetching all rows at once')
    cur.execute('SELECT * FROM cars')
    rows = cur.fetchall()
    for row in rows:
        print(row)


    print("Fetching rows one by one")
    cur.execute('SELECT * FROM cars ORDER BY id')
    while True:
        row = cur.fetchone() #after succesful call row is tuple of values 
        if row == None:
            break
        print(row)

    print('Using a dictionary cursor')
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM cars ORDER BY id')
    rows = cursor.fetchall()
    for i,row in enumerate(rows):
        print("Car {}".format(i + 1))
        print('Id {}'.format(row['id']))
        print('Name {}'.format(row['name']))
        print('Price {}'.format(row['price']))
        print('-'*30)

except psycopg2.DatabaseError as  e:

    print("Error {}".format(e))

finally:
    if con:
        con.close()


