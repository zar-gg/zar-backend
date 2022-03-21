
def query_gen(type, table, num_params):
    query_str = None
    if type == 'replace':
        query_str = '''REPLACE INTO {} VALUES '''.format(table)
        param_str = '({})'
        query_str += param_str.format(", ".join(['?' for _ in range(num_params)]))

    return query_str


def prepare_player_obj(data, stats):
    player_obj = {}

    player_obj['enc_puuid'] = data['puuid']
    player_obj['enc_id'] = data['id']
    player_obj['name'] = data['name']
    player_obj['level'] = data['summonerLevel']
    player_obj['iconId'] = data['profileIconId']
    player_obj['stats'] = stats

    return player_obj