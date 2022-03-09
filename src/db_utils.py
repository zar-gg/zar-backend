import sqlite3

def insert_or_replace(table, values):

    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    cur.execute(
        '''
        REPLACE INTO {} VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''.format(table), values
    )    
    
    conn.commit()
    conn.close()

def search(table, value):
    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name='{}'
        '''.format(table, value)
    )    
    
    print(*result)
    conn.close()

def match_key(table, region, key):
    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name LIKE '{}%' AND region='{}'
        '''.format(table, key, region)
    )    
    
    response = [*result]
    conn.close()
    return response 
