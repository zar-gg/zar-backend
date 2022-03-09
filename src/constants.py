class Constants:
    constant_dict = {
        "endpoints": {
            1: "/lol/summoner/v4/summoners/by-name/{}", #get player using player name
            2: "/lol/match/v5/matches/by-puuid/{}/ids", #get match history using player puuid
            3: "/lol/clash/v1/tournaments", #get list of current and upcoming clash tournaments
            4: "/lol/league/v4/entries/by-summoner/{}" #get player rank using their encrypted id
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
        "ddragon_versions": "https://ddragon.leagueoflegends.com/api/versions.json",
        "ddragon_region_version": "https://ddragon.leagueoflegends.com/realms/{}.json", #region_name
        "ddragon_endpoint": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/", #ddragon version
    }