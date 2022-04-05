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
        "id_queues": {
            "0":"custom_game",
            "72":"1v1_snowdown_showdown-howling_abyss",
            "73":"2v2_snowdown_showdown-howling-abyss",
            "75":"6v6_hexakill-summoners_rift",
            "76":"URF-summoners_rift",
            "78":"ofa_mirror_mode-howling_abyss",
            "83":"coop_vs_ai_urf-summoners_rift",
            "98":"6v6_hexakill-twisted_treeline",
            "100":"5v5_aram-butchers_bridge",
            "310":"nemesis_games-summoners_rift",
            "313":"black_market_brawlers-summoners_rift",
            "317":"definitely_not_dominion-crystal_scar",
            "325":"all_random-summoners_rift",
            "400":"normal_draft",
            "420":"ranked_solo",
            "430":"normal_blind",
            "440":"ranked_flex",
            "450":"5v5_aram-howling_abyss",
            "600":"blood_hunt_assasin-summoners_rift",
            "610":"dark_star_singularity-cosmic_ruins",
            "700":"clash",
            "820":"coop_vs_ai_beginner-twisted_treeline",
            "830":"coop_vs_ai_intro-summoners_rift",
            "840":"coop_vs_ai_beginner-summoners_rift",
            "850":"coop_vs_ai_intermediate-summoners_rift",
            "900":"arurf-summoners_rift",
            "910":"ascension-crystal_scar",
            "920":"legend_of_the_poro_king-howling_abyss",
            "940":"nexus_seige-summoners_rift",
            "1020":"ofa-summoners_rift",
            "1090":"tft_normal-convergence",
            "1100":"tft_ranked-convergence",
            "1110":"tft_tutorial-convergence",
            "1300":"nexus_blitz-nexus_blitz",
            "1400":"ultimate_spellbook-summoners_rift",
            "1900":"pick_urf-summoners_rift",
            "2000":"lol_tutorial_1-summoners_rift",
            "2010":"lol_tutorial_2-summoners_rift",
            "2020":"lol_tutorial_3-summoners_rift",
        },
        "ddragon_versions": "https://ddragon.leagueoflegends.com/api/versions.json", #returns array containing all versions
        "ddragon_region_version": "https://ddragon.leagueoflegends.com/realms/{}.json", #region_name (euw/na/kr)
        "ddragon_endpoint": "http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/", #ddragon version
    
        "table_cols": {
            "matches": "(region, match_id, enc_puuid)",
            "summoners": "(region, enc_puuid, name, enc_account_id, enc_summoner_id, level, profile_icon_id, revision_date, last_updated)",
            "ranked_stats": "(enc_puuid, flex_tier, flex_rank, flex_wins, flex_losses, flex_lp, flex_hotstreak, solo_tier, solo_rank, solo_wins, solo_losses, solo_lp, solo_hotstreak)",
            "teams": "(match_id, queue_type, riot_teamId, victorious, top, jungle, mid, adc, supp)",
            "match_details": "(match_id, queue_type, patch, winning_team, losing_team, match_created)",
        },
        "latest_patch":12,
    }
