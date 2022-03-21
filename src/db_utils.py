from utils import query_gen
import sqlite3

def insert_or_update(table, values):

    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    query = query_gen('replace', table, len(values))
    # cur.execute(
    #     '''
    #     REPLACE INTO {} VALUES 
    #     (?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     '''.format(table), values
    # )   
    cur.execute(query, values)     
    
    conn.commit()
    conn.close()

def player_search(table, value):
    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name='{}'
        '''.format(table, value)
    )    
    
    print(*result)
    conn.close()

def match_players(table, region, key):
    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name LIKE '{}%' AND region='{}' LIMIT 4
        '''.format(table, key, region)
    )    
    
    response = [*result]
    conn.close()
    return response 
