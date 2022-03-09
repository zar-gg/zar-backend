import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('./test_db/test.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE summoners
                (   
                    region text,
                    enc_puuid text PRIMARY KEY,
                    name text, 
                    enc_account_id text, 
                    enc_summoner_id text, 
                    level text, 
                    profile_icon_id text, 
                    revision_date integer, 
                    last_updated integer,
                    UNIQUE(region, enc_puuid, name)
                )
                ''')
