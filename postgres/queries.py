import psycopg2
import psycopg2.extras

con = None
dbname = 'pos'
username = 'blaz'
try:
    con = psycopg2.connect(database=dbname, user=username)
    cur = con.cursor()

    uid = 1
    uprice = 39999
    uname = 'Zaporozec'
    cur.execute('''
        UPDATE cars  SET 
                name = %s,
                price = %s
        WHERE id = %s
    ''',(uname, uprice, uid))

    con.commit()
    print('Car price 1  was updated')
    #the next example uses python parametrized queries
    uvalues = {'id':2, 'price': 3212}
    sSql = '''
        UPDATE cars SET price = %(price)s
        WHERE id = %(id)s
    '''
    cur.execute(sSql,uvalues)
    con.commit()
    print('Car price 2  was updated')

except psycopg2.DatabaseError as  e:

    print("Error {}".format(e))

finally:
    if con:
        con.close()

# Passing parameters to SQL queries
# 
# Psycopg casts Python variables to SQL literals by type. Many standard Python types are already adapted to the correct SQL representation.
# 
# Example: the Python function call:
# 
# >>> cur.execute(
# ...     """INSERT INTO some_table (an_int, a_date, a_string)
# ...         VALUES (%s, %s, %s);""",
# ...     (10, datetime.date(2005, 11, 18), "O'Reilly"))
# 
# is converted into the SQL command:
# 
# INSERT INTO some_table (an_int, a_date, a_string)
#  VALUES (10, '2005-11-18', 'O''Reilly');
# 
# Named arguments are supported too using %(name)s placeholders. Using named arguments the values can be passed to the query in any order and many placeholders can use the same values:
# 
# >>> cur.execute(
# ...     """INSERT INTO some_table (an_int, a_date, another_date, a_string)
# ...         VALUES (%(int)s, %(date)s, %(date)s, %(str)s);""",
# ...     {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})
# 
