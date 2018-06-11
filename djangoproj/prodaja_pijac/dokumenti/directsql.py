from django.db import connection

def getJsonArtikel(idArtikla):

    cursor = connection.cursor()
    sql = '''select row_to_json (sifranti_artikel)  
        from sifranti_artikel where id = {} 
    '''.format(idArtikla)
    cursor.execute(sql)
    row= cursor.fetchone()
    return(row)


def getSkupineArtiklov():
    cursor = connection.cursor()
    sql = '''
        select row_to_json(sifranti_skupinaartikla) from 
        sifranti_skupinaartikla order by naziv
    '''
    cursor.execute(sql)
    rows= cursor.fetchall()
    #spremenim v obliko primerno za django json
    #postgres ovije dictionary vrstice v tuple
    l = []
    for r in rows:
        l.append(r[0])
    return(l)
