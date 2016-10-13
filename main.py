#!/usr/bin/python3
import requests
import re

ID_FILE = "IDs.txt"
API_ENDPOINT = "http://y9lw.com/hosted/rocketleague/rankapi.php"
OUTPUT_FILE = "ranks.txt"

def parse_id_file(file):
    f = open(file, 'r')
    return [a.strip().split(',') for a in f.readlines()]

def get_rank(platform, id, season=3):
    regex = "(.*)'s Ranks Season 3; 1v1: (\d*) \| 2v2: (\d*) \| 3v3 Solo: (\d*) \| 3v3: (\d*) \| More stats at bit\.ly\/RLTrackerNetwork"
    platform_str = "steam" if platform == 0 else "ps"
    response = requests.get("{}?user={}&plat={}&season={}".format(API_ENDPOINT, id, platform_str, season)).text
    parsed_data = list(re.findall(regex, response)[0])
    parsed_data.insert(1, str(platform))
    rank_sum = str(sum(int(x) for x in parsed_data[1:]))
    return parsed_data + list([rank_sum])

players = parse_id_file(ID_FILE)
output_str = ""
for player in players:
    output_str += ",".join(get_rank(int(player[0]), player[1])) + "\n"

f = open(OUTPUT_FILE, 'w')
f.write(output_str)