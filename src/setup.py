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
                    
                    FOREIGN KEY (enc_puuid) REFERENCES summoners (enc_puuid)
                )
                ''') 

    # cur.execute('''CREATE TABLE matches
    #             (
    #                 match_id text PRIMARY KEY,
    #                 region text,    
    #             )
    #             ''')

    cur.execute('''CREATE TABLE teams
                (   
                    id text PRIMARY KEY,
                    match_id text,
                    riot_teamId text,
                    victorious bool,
                    top text,
                    jungle text,
                    mid text,
                    adc text,
                    supp text,

                    FOREIGN KEY (match_id) REFERENCES matches (match_id)
                    FOREIGN KEY (top) REFERENCES player (id)
                    FOREIGN KEY (jungle) REFERENCES player (id)
                    FOREIGN KEY (mid) REFERENCES player (id)
                    FOREIGN KEY (adc) REFERENCES player (id)
                    FOREIGN KEY (supp) REFERENCES player (id)
                )
                ''')

    cur.execute('''CREATE TABLE player_ingame_details
                (   
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    enc_puuid text,
                    champ_id integer,
                    champLevel integer,
                    champName text,
                    lane text,

                    FOREIGN KEY (enc_puuid) REFERENCES summoners (enc_puuid)
                )
                ''')

    cur.execute('''CREATE TABLE matches
                (   
                    match_id text PRIMARY KEY,
                    queue_type text,
                    patch text,
                    winning_team text,
                    losing_team text,
                    match_duration integer,
                    match_created integer,

                    FOREIGN KEY (winning_team) REFERENCES teams (id)
                    FOREIGN KEY (losing_team) REFERENCES teams (id)
                )
                ''')

    cur.execute('''CREATE TABLE version_data
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    latest_version text,
                    last_updated integer
                )
                ''')

    conn.close()
