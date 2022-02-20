class Constants:
    constant_dict = {
        "endpoints": {
            1: "/lol/summoner/v4/summoners/by-name/{}", #get player using player name
            2: "/lol/match/v5/matches/by-puuid/{}/ids", #get match history using player puuid
            3: "/lol/clash/v1/tournaments", #get list of current and upcoming clash tournaments
        },
        "regions":{
            "euw": "euw1",
            "na": "na1",
            "kr": "kr"
        }   
    }