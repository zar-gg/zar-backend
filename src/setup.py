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

    cur.execute('''CREATE TABLE ranked_stats
                (   
                    enc_puuid text PRIMARY KEY,
                    flex_tier text,
                    flex_rank text,
                    flex_wins integer,
                    flex_losses integer,
                    flex_lp integer,
                    flex_hotstreak,
                    solo_tier text,
                    solo_rank text,
                    solo_wins integer,
                    solo_losses integer,
                    solo_lp integer,
                    solo_hotstreak text,
                    FOREIGN KEY (enc_puuid)
                    REFERENCES summoners (enc_puuid)
                )
                ''') 

    cur.execute('''CREATE TABLE match_history
                (   
                    enc_puuid text PRIMARY KEY,
                    last_updated integer,
                    FOREIGN KEY (enc_puuid)
                    REFERENCES summoners (enc_puuid)
                )
                ''')

    conn.close()
