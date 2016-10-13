import requests

def get_steam_name_by_id(id, api_key):
    response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}".format(api_key, id))
    try:
        return response.json()['response']['players'][0]['personaname'].encode('utf-8')
    except:
        return None