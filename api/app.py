from flask import Flask, g
from flask_restful import Api
from resources.steam_player import SteamPlayer
from resources.ps4_player import PS4Player
from resources.player import Player
from resources.session import Session
from resources.keep_alive import KeepAlive
from common.database import Database
from db_url import db_url
import common.globals as globals

app = Flask(__name__)
api = Api(app)

globals.database = Database(db_url)
# set constants
globals.session_id, globals.steam_api_key = globals.database.get_constants()

@app.after_request
def headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

api.add_resource(Player, '/player', '/player/')
api.add_resource(SteamPlayer, '/player/steam', '/player/steam/<string:id>')
api.add_resource(PS4Player, '/player/ps4', '/player/ps4/<string:id>')
api.add_resource(Session, '/session', '/session/')
api.add_resource(KeepAlive, '/keepalive', '/keepalive/')

app.run(host="0.0.0.0", threaded=True)
