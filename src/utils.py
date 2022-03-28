
def query_gen(type, table, num_params):
    query_str = None
    if type == 'replace':
        query_str = '''REPLACE INTO {} VALUES '''.format(table)
        param_str = '({})'
        query_str += param_str.format(", ".join(['?' for _ in range(num_params)]))

    return query_str
