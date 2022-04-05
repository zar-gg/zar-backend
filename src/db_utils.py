import sqlite3

def query_gen(type, table, num_params, cols):
    query_str = None
    if type == 'replace':
        query_str = '''REPLACE INTO {} {} VALUES '''.format(table, cols)
        param_str = '({})'
        query_str += param_str.format(", ".join(['?' for _ in range(num_params)]))

    elif type == 'ignore':
        query_str = '''INSERT or IGNORE  INTO {} {} VALUES '''.format(table, cols)
        param_str = '({})'
        query_str += param_str.format(", ".join(['?' for _ in range(num_params)]))

    return query_str

def insert(table, values, type, cols=None, db_path='./src/test_db/test.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    if cols:
        query = query_gen(type, table, len(values), cols)
    else:
        query = query_gen(type, table, len(values))

    cur.execute(query, values)     
    
    conn.commit()
    conn.close()

def player_search(table, value, db_path='./src/test_db/test.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name='{}'
        '''.format(table, value)
    )    
    
    print(*result)
    conn.close()

def match_players(table, region, key, db_path='./src/test_db/test.db'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    result = cur.execute(
        '''
        SELECT * FROM {} WHERE name LIKE '{}%' AND region='{}' LIMIT 4
        '''.format(table, key, region)
    )    
    
    response = [*result]
    conn.close()
    return response 
