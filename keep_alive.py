import requests
import time
import urlparse
import psycopg2 
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_ENDPOINT = "https://psyonix-rl.appspot.com/"
UPDATE_ENDPOINT  = "Population/UpdatePlayerCurrentGame/"

urlparse.uses_netloc.append("postgres")
with open("db_url.txt", "r") as f:
    DB_URL = f.read().replace('\n', '')
if not DB_URL:
    print("Put the database url in db_url.txt")
    quit()
url = urlparse.urlparse(DB_URL)

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

def get_session():
    cur = conn.cursor()
    cur.execute("SELECT session_id FROM constants")
    data = cur.fetchone()
    cur.close()
    return data[0]


def keep_alive(session_id):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "SessionID" : session_id
    }
    body = {
        "PlaylistID": 0,
        "NumLocalPlayers": 1
    }
    response = requests.post(API_ENDPOINT + UPDATE_ENDPOINT, headers=headers, data=body, verify=False)

session_id = ""
while True:
    print("Updating session. Current: " + session_id)
    session_id = get_session()
    print("New: " + session_id)
    print("Sending keep alive")
    keep_alive(session_id)
    print("Waiting one minute")
    time.sleep(60 * 1) # sleep for one minute