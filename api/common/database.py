import os
import psycopg2
import urlparse
import requests

class Database:
    def __init__(self, db_url):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(db_url)
        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

    def get_constants(self):
        cur = self.conn.cursor()
        cur.execute("SELECT session_id, steam_api_key FROM constants")
        data = cur.fetchone()
        cur.close()
        return data

    def upsert_player(self, player):
        cur = self.conn.cursor()
        columns_str = ""
        values_str = ""
        for key, value in player.items():
            columns_str += "\"" + key + "\"" + ","
            values_str += "'" + str(value) + "'"  + ","
        columns_str += "\"last_update\""
        values_str += "now()"
        # TODO: pass parameters properly to escape them (test: 76561198065476197)
        cur.execute("INSERT INTO player ({0}) VALUES ({1}) ON CONFLICT (id) DO UPDATE SET ({0}) = ({1})".format(columns_str, values_str))
        self.conn.commit()
        cur.close()

    def get_players(self):
        cur = self.conn.cursor()
        cur.execute("SELECT \"id\", \"name\", \"platform\", \
                            \"1v1\", \"1v1_games_played\", \"1v1_tier\", \"1v1_division\", \"2v2\", \
                            \"2v2_games_played\", \"2v2_tier\", \"2v2_division\", \
                            \"3v3s\", \"3v3s_games_played\", \"3v3s_tier\", \"3v3s_division\", \
                            \"3v3\", \"3v3_games_played\", \"3v3_tier\", \"3v3_division\" \
                            FROM player")
        data = cur.fetchall()
        cur.close()
        return data

    def get_players_platform_id(self):
        cur = self.conn.cursor()
        cur.execute("SELECT platform, id FROM player")
        data = cur.fetchall()
        cur.close()
        return data
    
    def update_session(self, session_id):
        cur = self.conn.cursor()
        cur.execute("UPDATE constants SET session_id = %s", (session_id,))
        self.conn.commit()
        cur.close()