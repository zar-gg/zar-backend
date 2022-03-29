class Constants:
    constant_dict = {
        "endpoints": {
            1: "/lol/summoner/v4/summoners/by-name/{}", #get player using player name
            2: "/lol/match/v5/matches/by-puuid/{}/ids", #get match history using player puuid
            3: "/lol/clash/v1/tournaments", #get list of current and upcoming clash tournaments
            4: "/lol/league/v4/entries/by-summoner/{}", #get player rank using their encrypted id
            5: "/lol/match/v5/matches/{}", #get match details using match_id
        },
        "regions": {
            "euw": "euw1",
            "na" : "na1",
            "kr" : "kr",
        },
        "regions_match_history": {
            "na" : "americas",
            "euw": "europe",
            "kr" : "asia",
        },
        "queue_ids": {
            "normal_blind": "430",
            "normal_draft": "400",
            "ranked_solo" : "420",
            "ranked_flex" : "440",
            "clash"       : "700",
        },
        "ddragon_versions": "https://ddragon.leagueoflegends.com/api/versions.json", #returns array containing all versions
        "ddragon_region_version": "https://ddragon.leagueoflegends.com/realms/{}.json", #region_name (euw/na/kr)
        "ddragon_endpoint": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/", #ddragon version
    
        "table_cols": {
            "matches": "(region, match_id, enc_puuid)",
            "summoners": "(region, enc_puuid, name, enc_account_id, enc_summoner_id, level, profile_icon_id, revision_date, last_updated)",
            "ranked_stats": "(enc_puuid, flex_tier, flex_rank, flex_wins, flex_losses, flex_lp, flex_hotstreak, solo_tier, solo_rank, solo_wins, solo_losses, solo_lp, solo_hotstreak)",
            "teams": "(match_id, queue_type, riot_teamId, victorious, top, jungle, mid, adc, supp)",
            "match_details": "(match_id, queue_type, winning_team, losing_team)",
        }

    }
    