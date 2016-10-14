import urlparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__API_ENDPOINT = "https://psyonix-rl.appspot.com/"
__CALLPROC_ENDPOINT = "callproc105/"
__UPDATE_ENDPOINT  = "Population/UpdatePlayerCurrentGame/"

__PLAYLIST_MAP = {
        "10": "1v1",
        "11": "2v2",
        "12": "3v3s",
        "13": "3v3"
}

def __get_headers(session_id):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "SessionID" : session_id
    }

def __get_rp_from_mmr(mmr):
    return int(round(mmr * 20 + 100))

def __extract_rank(parsed_line):
    playlist = __PLAYLIST_MAP[parsed_line['Playlist'][0]]
    rp = __get_rp_from_mmr(float(parsed_line['MMR'][0]))
    rank = {}
    rank[playlist] = rp
    rank[playlist + "_games_played"] = int(parsed_line['MatchesPlayed'][0])
    rank[playlist + "_tier"] = int(parsed_line['Tier'][0])
    rank[playlist + "_division"] = int(parsed_line['Division'][0])
    return rank

def keep_alive(session_id):
    headers = __get_headers()
    body = {
        "PlaylistID": 0,
        "NumLocalPlayers": 1
    }
    response = requests.post(__API_ENDPOINT + __UPDATE_ENDPOINT, headers=headers, data=body, verify=False)

def get_ranks_by_id(platform, id, session_id):
    headers = __get_headers(session_id)

    body = {
        "Proc[]": "GetPlayerSkillSteam" if platform == 0 else "GetPlayerSkillPS4",
        "P0P[]": id
    }
    response = requests.post(__API_ENDPOINT + __CALLPROC_ENDPOINT, headers=headers, data=body, verify=False)

    # Invalid session
    if response.text.strip() == "SCRIPT ERROR SessionNotActive:" or response.text.strip() == "":
        return None
    
    ranks = {}
    lines = response.text.strip().split("\r\n")
    for line in lines[1:]:
        parsed_line = urlparse.parse_qs(line)
        rank_obj = __extract_rank(parsed_line)
        ranks.update(rank_obj)
    return ranks
