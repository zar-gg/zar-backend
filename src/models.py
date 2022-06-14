from constants import Constants

class Summoner:
    def __init__(self, puuid, username, teamId, lane, champ, kills, deaths, assists):
        self.puuid = puuid
        self.lane = lane
        self.champ = champ
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.kda = (kills + assists) / deaths

class Champion:
    def __init__(self, name, mastery, level):
        self.name = name
        self.mastery = mastery
        self.level = level

class Team:
    def __init__(self, match_id, riot_teamId, victorious, top, jgl, mid, adc, supp):
        self.match_id = match_id
        self.side = Constants.constant_dict[int(riot_teamId)]
        self.riot_teamId = riot_teamId
        self.victorious = victorious
        self.top = top
        self.jgl = jgl
        self.mid = mid
        self.adc = adc
        self.supp = supp

